from Domain import EntityValue


class ZoovuEntity:

    def __init__(self):
        self.values: [] = []
        self.index: int = 0
        self.intent_index: int = 0
        self.type: str = ""

    def add_value(self, value: EntityValue):
        self.values.append(value)

    def get_name(self) -> str:
        return "{0}_entity_{1}{2}".format(self.type, self.intent_index, self.index)

    def to_dict(self) -> dict:
        return {
            "entity": self.get_name(),
            "values": [value.to_dict() for value in self.values]
        }