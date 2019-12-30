from Domain.Entity import Entity


class Node:

    def __init__(self):
        self.intent: str = ""
        self.entities: [] = []
        self.response: [str] = []
