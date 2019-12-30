from ClevererBot.Domain.QA import QA
from ClevererBot.Domain.FileReader import FileReader
import re

from Domain.EntityPool import EntityPool


class QACollection:
    def __init__(self):
        self.QA = []
        self.file_reader = FileReader()
        self.entity_pool = EntityPool()

    def file_to_qa(self, path):
        md = self.file_reader.read_file_from_path(path)
        print(md)
        for qa in md.split("##"):
            print(qa)
            if qa.strip() != "":
                qa = qa.strip()
                qa = re.sub("\n", "", qa)
                self.QA.append(QA(qa.split("?")[0], qa.split("?")[1], self.entity_pool))
        self.markdown_analysis()

    def markdown_analysis(self):
        f = open("QA.md","w+")
        for qa in self.QA:
            f.write(qa.analyze())
        f.close()

    def create_entities(self):
        #for qa in self.QA:
            #for ent in qa.question.create_entities():
                #self.entity_pool.ad_entity(ent)
        #self.entity_pool.find_synonyms()
        #asyncio.run(self.entity_pool.start_threads())

        self.markdown_analysis()
