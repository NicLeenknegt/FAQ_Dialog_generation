import datetime
import json
from urllib import request


class ConversationService:

    def __init__(self):
        self.url = 'http://localhost:5000/api/v2{0}'

    def send_message(self, embed_token: str, input: str, context: dict):
        message_body = {
            "config": {
                "embedToken": embed_token,
                "publishVersion": 0
            },
            "input": {
                "text": input
            },
            "context": context
        }
        print(message_body)
        req = request.Request(self.url.format("/conversation/{0}/message".format(embed_token)))
        req.add_header('Content-Type', 'application/json')
        req.add_header('zoovu-unst-test', 'true')
        body = json.dumps(message_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def create_conversation(self, embed_token: str):
        creation_body = {
            "config":
                {
                    "embedToken": embed_token,
                    "publishVersion": None
                },
            "context":
                {
                    "conversationId": "",
                    "entities": [],
                    "intents": [],
                    "resultNode": {},
                    "variables": []},
            "input": {}
        }
        req = request.Request(self.url.format("/conversation/create".format(embed_token)))
        req.add_header('Content-Type', 'application/json')
        req.add_header('zoovu-unst-test', 'true')
        body = json.dumps(creation_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def date_converter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()