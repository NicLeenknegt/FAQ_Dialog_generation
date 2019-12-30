from Service.ThesaurusService import ThesaurusService


class EntityValue:

    def __init__(self, value: str):
        self.dict_service = ThesaurusService()
        self.value = value
        self.synonyms = []

    def find_synonyms(self):
        self.synonyms = self.dict_service.get_adjective_synonym(self.value)

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "synonyms": self.synonyms
        }