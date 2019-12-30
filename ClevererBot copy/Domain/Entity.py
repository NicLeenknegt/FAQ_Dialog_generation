from ClevererBot.Service.ThesaurusService import ThesaurusService
import re
from Domain.SpacyNLSingleton import SpacyNLSingleton
import spacy
import asyncio

class Entity:
    def __init__(self, root: str):
        self.dict_service = ThesaurusService()
        self.root = root
        self.synonyms = []
        self.find_synonyms()

    def find_synonyms(self):
        self.synonyms = self.dict_service.get_synonyms(self.root)
        print(self.synonyms)

    def get_analysis(self):
        res = "\n{} :\n".format(self.root)
        for syn in self.synonyms:
            res += "\t - {} \n".format(syn)
        return res

    async def most_similar(self, word):
        return self.dict_service.get_adjective_synonym(word)

