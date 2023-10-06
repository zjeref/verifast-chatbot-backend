import eventlet

eventlet.monkey_patch()

import json
from flask import jsonify
from flask_restx import Namespace, Resource, reqparse

from general_util import setup_logger

try:
    import unzip_requirements
except ImportError:
    pass

chat_resource = Namespace('chat', description='Callback')

chat_invocation_logger = setup_logger("chat_invocations", "./chat_invocations.log")

response_map = {
    'Hi': {
        'text': 'Hello from verifast!',
        'images': []
    },
    'show image': {
        'text': 'here are the images',
        'images': [
            'https://images.unsplash.com/photo-1574144611937-0df059b5ef3e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZnVubnklMjBjYXR8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60',
            'https://images.unsplash.com/photo-1561948955-570b270e7c36?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2101&q=80']
    },
    'default': {
        'text': 'what else?',
        'images': []
    }
}


@chat_resource.route('/verifast', methods=['POST'])
class ChatEndpoint(Resource):
    def post(self):
        payload = reqparse.request.get_json()
        chat_invocation_logger.info(json.dumps(payload, indent=1))
        query = payload['query']

        if query in response_map:
            result = response_map[query]
        else:
            result = response_map['default']
        return jsonify(result)
