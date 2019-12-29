import spacy
from ClevererBot.Domain.SpacyNLSingleton import SpacyNLSingleton
from ClevererBot.Domain.Question import Question
import re

from Domain.EntityPool import EntityPool
from Domain.Entity import Entity


class QA:
    def __init__(self, question, answer, entity_pool):
        self.question = Question(question)
        self.answer = answer
        self.entity_pool = entity_pool

    def __str__(self):
        return self.question + " " + self.answer

    def analyze(self):
        nlp = SpacyNLSingleton().val
        doc = nlp(self.question.sentence)
        table = ""

        table += "\n\nTEXT | LEMMA | POS | TAG | DEP | SHAPE | ALPHA \n" \
                 "| ------------- |------------- | ------------- | ------------- " \
                 "| ------------- | ------------- | ------------- |\n"

        for token in doc:
            table += token.text + " | " + token.lemma_ + " | " + token.pos_ + " | " + re.sub("\|", "&#124;", token.tag_ )+ " | " + token.dep_ + " | " + token.shape_ + " | " + ("TRUE" if token.is_alpha else "FALSE") + " |\n"
            if token.pos_ == "NOUN" or token.pos_ == "ROOT" or token.pos_ == "PROPN":
                ent = Entity(token.text)
                self.question.entities.append(ent)
                self.entity_pool.ad_entity(ent)

        table += "## " + self.question.sentence + "\n### Entiteiten: "

        for entity in self.question.entities:
            print(entity)
            table += entity.root
            table += "\n  "
            for synonym in self.entity_pool.entities_dict[entity.root]:
                table += synonym + " - "
            table += "\n"
        print(len(self.entity_pool.entities_dict))
        return table

