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


@chat_resource.route('/verifast', methods=['POST'])
class ChatEndpoint(Resource):
    def post(self):
        payload = reqparse.request.get_json()
        chat_invocation_logger.info(json.dumps(payload, indent=1))
        return jsonify({"message": 'ok'})


