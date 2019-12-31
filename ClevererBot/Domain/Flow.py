import re

from Domain.FileWriter import FileWriter
from Domain.ZoovuIntent import ZoovuIntent
from Domain.EntityValue import EntityValue
from Domain.ZoovuEntity import ZoovuEntity
from Domain.Entity import Entity
from Domain.FileReader import FileReader
from Domain.Node import Node
from Domain.EntityPool import EntityPool
import json

class Flow:

    def __init__(self):
        self.entity_pool: EntityPool = EntityPool()
        self.nodes: Node = []
        self.file_reader = FileReader()
        self.entities: [] = []
        self.intents: [] = []

    def build_nodes(self):
        md = self.file_reader.read_file_from_path('/Users/nic/School/Bachelorproef/ClevererBot/ClevererBot/FAQ.md')
        responses = []

        for line in md.split("\n\n"):
            line = line.strip()
            if line.startswith("##"):
                intent: ZoovuIntent = ZoovuIntent()
                intent.index = len(self.intents)
                annotation = line.split("//")[1]
                annotation = annotation.replace("_", " ")

                #ENTITIES
                for ent in self.find_hard_entities(annotation, intent.index):
                    self.entities.append(ent)
                for ent in self.find_synonym_entities(annotation, intent.index):
                    self.entities.append(ent)

                #INTENT EXAMPLE
                annotation = self.format_annotation(annotation, "{", '}', intent.index, "synonym")
                annotation = self.format_annotation(annotation, "[", ']', intent.index, "hard")
                intent.value = annotation

                if responses:
                    self.intents[len(self.intents) - 1].insert_responses(responses)
                    responses = []

                self.intents.append(intent)

            else:
                res_lines: str = ""
                for res in line.split("\n"):
                    if res.strip() is not '':
                        res_lines = res_lines + res + " "
                    else:
                        responses.append(res_lines)
                        res_lines = ""
                responses.append(res_lines)

        if responses:
            self.intents[len(self.intents) - 1].insert_responses(responses)
            responses = []

        print(self.to_dict())
        with open('data.json', 'w') as json_file:
            json.dump(self.to_dict(), json_file)

    def format_annotation(self, annotation: str, left_format: str, right_format: str, intent_index: int,
                          ent_type: str) -> str:
        count: int = 0
        while annotation.__contains__(left_format) or annotation.__contains__(right_format):
            left: str = annotation.split(left_format)[0]
            right: str = ""
            if len(annotation.split(right_format)) > 1:
                right = annotation.split(right_format)[1]

            annotation = left + "@{0}_entity_{1}{2}".format(ent_type, intent_index, count) + right
            count += 1
       # print(annotation)
        return annotation

    def find_hard_entities(self, root: str, intent_index: int) -> []:
        return self.find_entities(root, r"\[(.+?)\]", "hard", intent_index)

    def find_synonym_entities(self, root: str, intent_index: int) -> []:
        entities = self.find_entities(root, r"{(.+?)}", "synonym", intent_index)
        for ent in entities:
            for value in ent.values:
                value.find_synonyms()

        return self.find_entities(root, r"{(.+?)}", "synonym", intent_index)

    def find_entities(self, root: str, rematch: str, ent_type: str, intent_index: int) -> []:
        matches: [] = re.findall(rematch, root)
        entities: [] = []
        index: int = 0
        for match in matches:
            entity: ZoovuEntity = ZoovuEntity()
            entity.type = ent_type
            entity.intent_index = intent_index
            match = str(match).strip().lower()

            if match != "":
                if match.__contains__(","):
                    for value in match.split(","):
                        entity.add_value(EntityValue(value))
                else:
                    result: bool = True
                    entity.add_value(EntityValue(match))

            if entity is not None:
                entity.index = index
                index = index + 1
                entities.append(entity)
        #print(entities)
        return entities

    def to_dict(self):
        return {
            'intents': [intent.to_dict() for intent in self.intents],
            'entities': [ent.to_dict() for ent in self.entities]
        }