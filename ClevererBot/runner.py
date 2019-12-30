from urllib.error import HTTPError
from Domain.Flow import Flow
import json
from Service.ChatbotService import ChatbotService


def main():
    flow: Flow = Flow()
    flow.build_nodes()

    build_entities(flow)
    build_intents(flow)
    build_chatbot_nodes(flow)


def build_entities(flow: Flow):
    print(flow.to_dict()["entities"][0])
    resp = ChatbotService().create_entities(flow.to_dict())
    entities = json.loads(resp)
    print(entities)
    for ent in entities['data']:
        for ent_dict in flow.entities:
            if ent['updatedEntity'] == ent_dict.get_name():
                try:
                    result_json = ChatbotService().add_value_to_entity(ent['_id'], ent_dict)
                    result = json.loads(result_json)
                    for entity in result['data']:
                        if entity['updatedEntity'] == ent_dict.get_name():
                            for value in entity['values']:
                                for ent_value in ent_dict.values:
                                    if ent_value.value == value['updatedValue']:
                                        if ent_dict.type == 'synonym':
                                            synonyms = ent_value.get_synonyms()
                                            if synonyms:
                                                ChatbotService().add_synonyms_to_entity_value(
                                                    ent['_id']
                                                    , value['_id']
                                                    , synonyms
                                                )
                except HTTPError:
                    print("ERROR occurred while adding values to entities")


def build_intents(flow: Flow):
    for intent in flow.intents:
        intent_dict = ChatbotService().create_intents(intent)
        intent_json = json.loads(intent_dict)
        try:
            ChatbotService().add_utterances_to_intent(intent_json["data"][0]["_id"], intent)
        except HTTPError:
            print("error when adding example to intent")


def build_chatbot_nodes(flow: Flow):
    ChatbotService().get_dialog_nodes()
    previous_sibling: str = None

    for intent in flow.intents:
        result = ChatbotService().add_dialog_node(previous_sibling, (intent.index + 1))
        result_json = json.loads(result)
        node_id: str = ""

        if previous_sibling is None:
            node_id = result_json['data'][1]['_id']
            previous_sibling = result_json['data'][0]['_id']
        else:
            for node in result_json['data']:
                if node['previousSibling'] == previous_sibling:
                    node_id = node['_id']
                    previous_sibling = node_id

        ChatbotService().set_dialog_node_title(node_id, "node_{0}".format((intent.index + 1)))
        res = ChatbotService().add_response_to_dialog_node(node_id)
        result_json = json.loads(res)

        for node in result_json['data']:
            if node['_id'] == node_id:
                response_id = node['singleResponse']["_id"]
                print(response_id)
                if intent.responses:
                    ChatbotService().add_text_to_response(node_id, response_id, intent)
                    ChatbotService().set_selection_policy_to_all(node_id, response_id)

        ChatbotService().add_node_condition(node_id, intent)


def most_similar(word):
    if (word and word.vector_norm):
        by_similarity = sorted(word.vocab, key=lambda w: word.similarity(w), reverse=True)
        return [w.orth_ for w in by_similarity[:10]]
    else:
        return []


main()
