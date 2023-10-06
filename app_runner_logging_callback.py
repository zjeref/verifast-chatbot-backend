import json
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_restful import Api, Resource


from general_util import setup_logger

try:
    import unzip_requirements
except ImportError:
    pass


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


class ChatEndpoint(Resource):
    def post(self):
        payload = request.get_json()
        chat_invocation_logger.info(json.dumps(payload, indent=1))
        query = payload['query']

        if query in response_map:
            result = response_map[query]
        else:
            result = response_map['default']
        return jsonify(result)


app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(ChatEndpoint, '/verifast')

if __name__ == '__main__':
    app.run(debug=True)  # Set debug to False in a production environment
