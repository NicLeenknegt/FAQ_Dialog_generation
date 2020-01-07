from urllib.error import HTTPError
from Domain.Flow import Flow
import json
from Service.ChatbotService import ChatbotService
from Service.ConversationService import ConversationService


def main():
    flow: Flow = Flow()
    flow.build_nodes()

    # new_chatbot_id = create_chatbot()
    new_chatbot_id = '5e0b32d05c2e9b8273579740'
    clear_field(new_chatbot_id)

    build_entities(new_chatbot_id, flow)
    build_intents(new_chatbot_id, flow)
    build_chatbot_nodes(new_chatbot_id, flow)
    train_bot(new_chatbot_id)


def create_chatbot() -> str:
    result_json = ChatbotService().create_chatbot({'name': 'test_4'})
    result = json.loads(result_json)
    return result['data']["botId"]


def clear_field(chatbot_id: str):
    result_json = ChatbotService().get_dialog_nodes(chatbot_id)
    result = json.loads(result_json)
    for node in result['data']:
        node_id = node["_id"]
        ChatbotService().delete_dialog_node(
            node['chatbotId'],
            node_id,
            node['previousSibling'],
            node['nextSibling'],
            node['position']
        )

    try:
        ChatbotService().add_dialog_node(chatbot_id, None, 0)
    except HTTPError:
        print("welcome node created")

    result_json = ChatbotService().get_dialog_nodes(chatbot_id)
    result = json.loads(result_json)
    for node in result['data']:
        node_id = node['_id']
        result_json = ChatbotService().add_response_to_dialog_node(chatbot_id, node_id)
        result = json.loads(result_json)
        for node in result['data']:
            if node['_id'] == node_id:
                response_id = node['singleResponse']["_id"]
                ChatbotService().add_text_to_response(
                    chatbot_id,
                    node_id,
                    response_id,
                    ['Well hello there']
                )


def build_entities(chatbot_id: str, flow: Flow):
    resp = ChatbotService().create_entities(chatbot_id, flow.to_dict())
    entities = json.loads(resp)
    for ent in entities['data']:
        for ent_dict in flow.entities:
            if ent['updatedEntity'] == ent_dict.get_name():
                try:
                    result_json = ChatbotService().add_value_to_entity(
                        chatbot_id,
                        ent['_id'],
                        ent_dict
                    )
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
                                                    chatbot_id,
                                                    ent['_id']
                                                    , value['_id']
                                                    , synonyms
                                                )
                except HTTPError:
                    print("ERROR occurred while adding values to entities")


def build_intents(chatbot_id: str, flow: Flow):
    for intent in flow.intents:
        intent_dict = ChatbotService().create_intents(chatbot_id, intent)
        intent_json = json.loads(intent_dict)
        try:
            ChatbotService().add_utterances_to_intent(chatbot_id, intent_json["data"][0]["_id"], intent)
        except HTTPError:
            print("error when adding example to intent")


def build_chatbot_nodes(chatbot_id: str, flow: Flow):
    previous_sibling: str = None

    for intent in flow.intents:
        result = ChatbotService().add_dialog_node(chatbot_id, previous_sibling, (intent.index + 1))
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

        ChatbotService().set_dialog_node_title(chatbot_id, node_id, "node_{0}".format((intent.index + 1)))
        res = ChatbotService().add_response_to_dialog_node(chatbot_id, node_id)
        result_json = json.loads(res)

        for node in result_json['data']:
            if node['_id'] == node_id:
                response_id = node['singleResponse']["_id"]
                if intent.responses:
                    ChatbotService().add_text_to_response(chatbot_id, node_id, response_id, intent.responses)
                    ChatbotService().set_selection_policy_to_all(chatbot_id, node_id, response_id)
        ChatbotService().add_node_condition(chatbot_id, node_id, intent)


def train_bot(chatbot_id: str):
    ChatbotService().train_watson(chatbot_id)


def most_similar(word):
    if (word and word.vector_norm):
        by_similarity = sorted(word.vocab, key=lambda w: word.similarity(w), reverse=True)
        return [w.orth_ for w in by_similarity[:10]]
    else:
        return []


def test():
    res = ConversationService().create_conversation("ck4tsqrx3000srnt5pzac8kjr")
    result_json = json.loads(res)
    context = result_json['data']['context']
    test_array = [
        {
            "intent": "intent_0",
            "examples": [
                "What is Selling On Amazon",
                "Tell me about selling on amazon",
                "Tell me how to sell on amazon"
            ]
        },
        {
            "intent": "intent_1",
            "examples": [
                "why sell on amazon",
                "Why should I sell on Amazon",
                "why trade on amazon"
            ]
        }
    ]

    result_array: [] = []

    for test in test_array:
        result: dict = {
            "intented_intent": test['intent'],
            "results": []
        }
        for example in test['examples']:
            res = ConversationService().send_message(
                "ck4tsqrx3000srnt5pzac8kjr",
                example,
                context
            )
            result_json = json.loads(res)
            result_intent = result_json['data']['context']['intents'][0]
            result_intent['example'] = example

            result['results'].append(result_intent)
        result_array.append(result)

    print(result_array)



# main()
test()
