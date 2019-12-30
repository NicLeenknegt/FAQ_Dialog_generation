
class ZoovuIntent:

    def __init__(self):
        self.index: int = 0
        self.value: str = ""
        self.responses = []

    def get_name(self):
        return "intent_{0}".format(self.index)

    def to_dict(self) -> dict:
        return {
                "intent": self.get_name(),
                "examples": {
                    "text": self.value
                },
                "responses": {
                    "text": [resp for resp in self.responses]
                }
            }

    def get_intent(self) -> dict:
        return {
            "intent": self.get_name()
        }

    def get_example(self) -> []:
        return [
            {
                'text': self.value
            }
        ]

    def insert_responses(self, resp: []):
        self.responses = self.responses + resp

    def get_condition(self):
        return "# intent_{0}".format(self.index)