
class ZoovuIntent:

    def __init__(self):
        self.index: int = 0
        self.value: str = ""

    def get_name(self):
        return "intent_{0}".format(self.index)

    def to_dict(self) -> dict:
        return {
                "intent": self.get_name(),
                "examples": {
                    "text": self.value
                }
            }
