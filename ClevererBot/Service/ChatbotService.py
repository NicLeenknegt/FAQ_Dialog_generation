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
        req = request.Request(self.url.format("/chatbot/5e09d9fa43902d102a7af3f5/import?intents=true&entity=true"),
                              data)
        resp = request.urlopen(req)
        return resp.read()

    def create_entities(self, chatbot_id: str, entities: dict):
        req = request.Request(self.url.format(
            "/chatbot/{0}/entity".format(chatbot_id)
        ))
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(entities)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_value_to_entity(self, chatbot_id: str, entity_id: str, entity: ZoovuEntity):
        values = entity.get_values()
        req = request.Request(self.url.format(
            "/chatbot/{0}/entity/{1}/value".format(
                chatbot_id,
                entity_id
            )))
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(values)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def create_intents(self, chatbot_id: str, intent: ZoovuIntent):
        intent_body: dict = {"intent": intent.get_intent()}

        req = request.Request(self.url.format("/chatbot/{0}/intent".format(chatbot_id)))
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(intent_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_utterances_to_intent(self, chatbot_id: str, intent_id: str, intent: ZoovuIntent):
        utterance_body = {"examples": intent.get_example()}

        req = request.Request(self.url.format("/chatbot/{0}/intent/{1}/example"
                                              .format(chatbot_id, intent_id)))
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(utterance_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def get_dialog_nodes(self, chatbot_id: str):
        req = request.Request(self.url.format("/chatbot/{0}/dialogNode"
                                              .format(chatbot_id)))
        req.add_header('Content-Type', 'application/json')

        resp = request.urlopen(req)
        return resp.read()

    def delete_dialog_node(self, chatbot_id: str, dialog_node_id: str, previous_sibling: str, next_sibling: str,
                           position: int):
        node_body = {
            "dialogNodeId": dialog_node_id,
            'deletable': [
                {
                    '_id': dialog_node_id,
                    'previousSibling': previous_sibling,
                    'nextSibling': next_sibling,
                    'chatbotId': chatbot_id,
                    'position': position
                }
            ]
        }

        req = request.Request(self.url.format(
            "/chatbot/5e09d9fa43902d102a7af3f5/dialogNode/{0}".format(dialog_node_id)),
            method='DELETE'
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_dialog_node(self, chatbot_id: str, previous_sibling: str, position: int):
        node_body = {
            "dialogNode":
                {
                    'previousSibling': previous_sibling,
                    'position': position
                }
        }

        req = request.Request(self.url.format("/chatbot/{0}/dialogNode".format(chatbot_id)))
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def set_dialog_node_title(self, chatbot_id: str, dialog_node_id: str, dialog_node_title: str):
        node_body = {
            'dialogNodeId': dialog_node_id,
            'node': {
                'title': dialog_node_title,
                'description': ''
            }
        }
        req = request.Request(
            self.url.format("/chatbot/{0}/dialogNode/{1}".format(chatbot_id, dialog_node_id)),
            method='PUT'
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_response_to_dialog_node(self, chatbot_id: str, dialog_node_id: str):
        node_body = {
            'dialogNodeId': dialog_node_id,
            'responseType': 'TEXT'
        }
        req = request.Request(
            self.url.format("/chatbot/{0}/dialogNode/{1}/response".format(chatbot_id, dialog_node_id))
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_text_to_response(self, chatbot_id: str, dialog_node_id: str, response_id: str, responses: []):
        node_body = {
            'dialogNodeId': dialog_node_id,
            'responseId': response_id,
            'texts': responses
        }
        req = request.Request(
            self.url.format("/chatbot/{0}/dialogNode/{1}/response/{2}/responseText"
                            .format(chatbot_id, dialog_node_id, response_id))
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def set_selection_policy_to_all(self, chatbot_id: str, dialog_node_id: str, response_id: str, ):
        node_body = {
            'dialogNodeId': dialog_node_id,
            'responseId': response_id,
            'selectionPolicy': 'ALL'
        }
        req = request.Request(
            self.url.format("/chatbot/{0}/dialogNode/{1}/response/{2}"
                            .format(chatbot_id, dialog_node_id, response_id)),
            method='PUT'
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_node_condition(self, chatbot_id: str, dialog_node_id: str, intent: ZoovuIntent):
        node_body = {
            'dialogNodeId': dialog_node_id,
            'conditions': {'conditionData': intent.get_condition()}
        }
        req = request.Request(
            self.url.format("/chatbot/{0}/dialogNode/{1}/nodeCondition"
                            .format(chatbot_id, dialog_node_id))
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def add_synonyms_to_entity_value(self, chatbot_id: str, entity_id: str, value_id: str, synonyms: []):
        node_body = {
            'entityId': entity_id,
            'valueId': value_id,
            'synonyms': synonyms,
            'searchText': ''
        }
        req = request.Request(
            self.url.format("/chatbot/{0}/entity/{1}/value/{2}/synonym"
                            .format(chatbot_id, entity_id, value_id))
        )
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(node_body)
        body_as_bytes = body.encode('utf-8')
        resp = request.urlopen(req, body_as_bytes)
        return resp.read()

    def train_watson(self, chatbot_id: str):
        req = request.Request(
            self.url.format("/chatbot/{0}/trainWatson"
                            .format(chatbot_id)),
            method='POST'
        )
        req.add_header('Content-Type', 'application/json')
        resp = request.urlopen(req)
        return resp.read()