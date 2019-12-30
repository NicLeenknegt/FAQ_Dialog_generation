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

from Service.ChatbotService import ChatbotService


def main():
    #fileReader = FileReader()

    flow: Flow = Flow()
    flow.build_nodes()
    #ChatbotService().create_chatbot({'name': 'test'})
    #ChatbotService().import_intents_entities(flow.to_dict())
    print(flow.to_dict()["entities"][0])
    ChatbotService().create_entities(flow.to_dict())

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

def most_similar(word):
    if (word and word.vector_norm):
        by_similarity = sorted(word.vocab, key=lambda w: word.similarity(w), reverse=True)
        return [w.orth_ for w in by_similarity[:10]]
    else:
        return []
main()