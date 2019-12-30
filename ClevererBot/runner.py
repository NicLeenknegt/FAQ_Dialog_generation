from urllib.error import HTTPError

from ClevererBot.Domain.FileReader import FileReader
import html2text
import urllib.request
from Domain.FileWriter import FileWriter
from Domain.Flow import Flow
from Service.BaseService import BaseService
from Domain.QACollection import QACollection
from ClevererBot.Service.ThesaurusService import ThesaurusService
from ClevererBot.Service.MijnWoordenboekService import MijnWoordenboekService
import re
from Domain.SpacyNLSingleton import SpacyNLSingleton
import spacy
import json

from Service.ChatbotService import ChatbotService


def main():
    #fileReader = FileReader()

    flow: Flow = Flow()
    flow.build_nodes()
    #ChatbotService().create_chatbot({'name': 'test'})
    #ChatbotService().import_intents_entities(flow.to_dict())

    #=====IMPORTANT=====
    #print(flow.to_dict()["entities"][0])
    #resp = ChatbotService().create_entities(flow.to_dict())
    #entities = json.loads(resp)
    #print(entities)
    #for ent in entities['data']:
     #   for ent_dict in flow.entities:
      #      if ent['updatedEntity'] == ent_dict.get_name():
       #         try:
        #            ChatbotService().add_value_to_entity(ent['_id'], ent_dict)
         #       except HTTPError:
          #          print("ERROR occurred while adding values to entities")
    # =====IMPORTANT=====
    #for intent in flow.intents:
     #   intent_dict = ChatbotService().create_intents(intent)
      #  intent_json = json.loads(intent_dict)
       # print(intent_json)
        #print(intent_json["data"][0]["_id"])
       # try:
       #     ChatbotService().add_utterances_to_intent(intent_json["data"][0]["_id"], intent)
       # except HTTPError:
        #    print("error when adding example to intent")
   # result = ChatbotService().get_dialog_nodes()
    #result_json = json.loads(result)
    #print(result_json)
    #for res in result_json['data']:
      #  print(res['title'])
       # print(res['position'])
    build_chatbot_nodes(flow)



    #qa_col = QACollection()
    #qa_col.file_to_qa('/Users/nic/School/Bachelorproef/ClevererBot/ClevererBot/FAQ.md')
    #nlp = spacy.load("nl_vectors_web_lg")
    #dict = MijnWoordenboekService()
    #print(dict.get_synonym_list("mooi"))
   # h = html2text.HTML2Text()
    #h.ignore_links = True
    #md = h.handle(dict.word_synonym("mooi").decode())
    # print(dict.word_synonym("mooi").decode())
    #html = re.findall("<h2>Synoniemen van.+<ul.+>.+</ul><h2>P", dict.word_synonym("mooi").decode(), re.DOTALL)[0]
    #for a in re.findall("<a.+?>.+?</a>", html):
    #    print(re.sub("<.+?>","", a))

    #[print(m) for m in answers.split(":_:")]
    ##qaCol = fileReader.markdownToQA(f)
    ##qaCol.markdownAnalysys()

    #ts = ThesaurusService()
    #print(ts.get_adjective_synonym("nice"))

    #uf = urllib.request.urlopen("https://words.bighugelabs.com/api/2/160285b81fbaef0b961c03fe884a0efa/nice/json")
    #print(uf.read())
    #uf = urllib.request.urlopen("https://services.amazon.com/selling/faq.html")
    #h = html2text.HTML2Text()
    #h.ignore_links = True
    #html = uf.read()
    #md = h.handle(html.decode())
    #print(type(md))
    #questions = re.findall("#.+\?", md)
    #occurences = []
    #for q in questions:
    #    for pat in re.findall("^(#+)", q):
    #        occurences.append(pat)
    #print(occurences)


    #FileWriter().write_file("FAQ.md", [md])

def build_chatbot_nodes(flow:Flow):
    result = ChatbotService().get_dialog_nodes()
    result_json = json.loads(result)
    print(result_json)

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
                    print("second")
                    print(previous_sibling)

        ChatbotService().set_dialog_node_title(node_id, "node_{0}".format((intent.index + 1)))
        res = ChatbotService().add_response_to_dialog_node(node_id)
        result_json = json.loads(res)

        for node in result_json['data']:
            if node['_id'] == node_id:
                response_id = node['singleResponse']["_id"]
                print(response_id)
                if intent.responses:
                    ChatbotService().add_text_to_response(node_id, response_id, intent)


def most_similar(word):
    if (word and word.vector_norm):
        by_similarity = sorted(word.vocab, key=lambda w: word.similarity(w), reverse=True)
        return [w.orth_ for w in by_similarity[:10]]
    else:
        return []
main()