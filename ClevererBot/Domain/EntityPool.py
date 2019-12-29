import asyncio
import spacy

from Domain.Entity import Entity


class EntityPool:
    def __init__(self):
        self.entities_dict = {}
        self.nlp = spacy

    def ad_entity(self, ent: Entity):
        if ent.root not in self.entities_dict:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(ent.find_synonyms())
            self.entities_dict[ent.root] = ent.synonyms

    async def find_synonyms(self):
        for ent in self.entities_dict:
            await ent.find_synonyms()

    async def start_threads(self):
        divide = 3
        border = int(len(self.entities_dict) / divide)
        threads = []

        for x in range(divide - 2):
            threads.append(self.entities_dict[x * border:(x + 1) * border])
        threads.append(self.entities_dict[(divide - 1) * border:len(self.entities_dict) - 1])

        await asyncio.gather(*[self.execute_threads(t) for t in threads])
        for ent in self.entities_dict:
            print(ent)

    async def execute_threads(self, ents):
        for ent in ents:
            await ent.find_synonyms()