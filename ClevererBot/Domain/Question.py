import asyncio

import spacy
from ClevererBot.Domain.SpacyNLSingleton import SpacyNLSingleton
import spacy
from Domain.Entity import Entity
class Question:

    def __init__(self, sentence):
        self.sentence = sentence
        self.entities = []


    def __str__(self):
        return self.sentence

    def create_entities(self):
        nlp = SpacyNLSingleton().val
        doc = nlp(self.sentence)
        print("ENTITY_CREATION")
        for token in doc:
            if token.pos_ == "NOUN" or token.pos_ == "ROOT" or token.pos_ == "PROPN":
                ent = Entity(token.text)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(ent.find_synonyms())

                self.entities.append(ent)
            # if token.dep_ == "ROOT":
            #     for root_child in token.children:
            #         if root_child.pos_ == "CONJ":
            #             if root_child.text not in self.entities:
            #                 entities.append(Entity(root_child.text))
        return self.entities
