from ClevererBot.Service.BaseService import BaseService
from ClevererBot.Utils.JsonReader import JsonReader
from ClevererBot.Domain.Enum.ThesaurusWordTypeEnum import ThesaurusWordType
import json
class ThesaurusService:

    def __init__(self):
        self.base_service = BaseService()
        self.json_reader = JsonReader()

    @BaseService.send_url_request("https://words.bighugelabs.com/api/2/60a52e78e79d1b0fc3f9915694f52a55/{0}/json")
    def word_synonym(self, word):
        print("Word_check")
        print(word)
        return word

    def get_synonym_json(self, word):
        word = word.strip()
        if word != "":
            response = self.word_synonym(word)
            if response != None:
                return json.loads(response.decode())
            else:
                return {}
        else:
            return {}

    def get_synonyms(self, word):
        json_obj = self.json_reader.read_attribute(self.get_synonym_json(word))
        syn = [[]]
        res = []
        if json_obj is []:
            syn.append(json_obj)
        else:
            syn.append(self.json_reader.read_attribute(json_obj, 'noun', 'syn'))
            syn.append(self.json_reader.read_attribute(json_obj, 'verb', 'syn'))
            syn.append(self.json_reader.read_attribute(json_obj, 'adverb', 'syn'))
            syn.append(self.json_reader.read_attribute(json_obj, 'adjective', 'sim'))
        for s in syn:
            if s is not None:
                res = res + s
        return res

    def get_adjective_synonym(self, word):
        return self.get_synonyms(word, ThesaurusWordType.ADJECTIVE)

    def get_noun_synonym(self, word):
        return self.get_synonyms(word, ThesaurusWordType.NOUN)