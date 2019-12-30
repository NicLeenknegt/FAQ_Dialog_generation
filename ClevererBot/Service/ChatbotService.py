from urllib import parse, request
import json

from Domain.ZoovuEntity import ZoovuEntity
from Domain.ZoovuIntent import ZoovuIntent


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
        req = request.Request(self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/import?intents=true&entity=true"),data)
        resp = request.urlopen(req)
        return resp.read()

    def create_entities(self, entities: dict):
        req = request.Request(self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/entity"))
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(entities)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_value_to_entity(self, entity_id: str, entity: ZoovuEntity):
        values = entity.get_values()
        req = request.Request(self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/entity/{0}/value".format(entity_id)))
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(values)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def create_intents(self, intent: ZoovuIntent):
        intent_body: dict = {"intent": intent.get_intent()}

        req = request.Request(self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/intent"))
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(intent_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_utterances_to_intent(self, intent_id: str, intent: ZoovuIntent):
        utterance_body = { "examples": intent.get_example() }

        req = request.Request(self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/intent/{0}/example".format(intent_id)))
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(utterance_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def get_dialog_nodes(self):
        req = request.Request(self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/dialogNode"))
        req.add_header('Content-Type', 'application/json')

        resp = request.urlopen(req)
        return resp.read()

    def add_dialog_node(self, previous_sibling: str, position: int):

        node_body = {
            "dialogNode":
                {
                    'previousSibling': previous_sibling,
                    'position': position
            }
        }

        req = request.Request(self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/dialogNode"))
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def set_dialog_node_title(self, dialog_node_id: str, dialog_node_title:  str):
        node_body = {
            'dialogNodeId': dialog_node_id,
            'node': {
                'title': dialog_node_title,
                'description': ''
            }
        }
        req = request.Request(
            self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/dialogNode/{0}".format(dialog_node_id)),
            method='PUT'
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_response_to_dialog_node(self, dialog_node_id: str):
        node_body = {
            'dialogNodeId': dialog_node_id,
            'responseType': 'TEXT'
        }
        req = request.Request(
            self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/dialogNode/{0}/response".format(dialog_node_id))
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_text_to_response(self, dialog_node_id: str, response_id: str, intent: ZoovuIntent):
        node_body = {
            'dialogNodeId': dialog_node_id,
            'responseId': response_id,
            'texts': intent.responses
        }
        req = request.Request(
            self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/dialogNode/{0}/response/{1}/responseText"
                            .format(dialog_node_id, response_id))
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def set_selection_policy_to_all(self, dialog_node_id: str, response_id: str,):
        node_body = {
            'dialogNodeId': dialog_node_id,
            'responseId': response_id,
            'selectionPolicy': 'ALL'
        }
        req = request.Request(
            self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/dialogNode/{0}/response/{1}"
                            .format(dialog_node_id, response_id)),
            method='PUT'
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_node_condition(self, dialog_node_id: str, intent:ZoovuIntent ):
        node_body = {
            'dialogNodeId': dialog_node_id,
            'conditions': {'conditionData': intent.get_condition()}
        }
        req = request.Request(
            self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/dialogNode/{0}/nodeCondition"
                            .format(dialog_node_id))
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_synonyms_to_entity_value(self, entity_id: str, value_id: str, synonyms: []):
        node_body = {
            'entityId': entity_id,
            'valueId': value_id,
            'synonyms': synonyms,
            'searchText': ''
        }
        req = request.Request(
            self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/entity/{0}/value/{1}/synonym"
                            .format(entity_id, value_id))
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()