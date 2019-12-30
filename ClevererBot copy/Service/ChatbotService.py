from urllib import parse, request
import json

class ChatbotService:

    def __init__(self):
        self.url = 'http://localhost:5000/api/v1{0}'


    # name:str
    def create_chatbot(self, body: dict):
        body["assistantCode"] = "123"
        body["locale"] = "en"
        data = parse.urlencode(body).encode()
        req = request.Request(self.url.format("/assistant"), data)
        resp = request.urlopen(req)
        return resp.read()

    def import_intents_entities(self, body: dict):
        body["query"] = body
        data = parse.urlencode(body).encode("utf-8")
        req = request.Request(self.url.format("/chatbot/5dfb3e7b57fd2b22058206d9/import?intents=true&entity=true"),data)
        resp = request.urlopen(req)
        return resp.read()

    def create_entities(self, entities: dict):
        req = request.Request(self.url.format("/chatbot/5d4986a840dfe24f7c425c73/entity"))
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(entities)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()