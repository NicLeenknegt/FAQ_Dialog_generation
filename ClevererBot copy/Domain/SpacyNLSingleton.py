import spacy
import re

class SpacyNLSingleton:

    class __SPacySingleton:
        def __init__(self):
            self.val = spacy.load('nl_core_news_sm')

        def __str__(self):
            return 'self' + self.val

    instance = None

    def __new__(cls, *args, **kwargs):
        if not SpacyNLSingleton.instance:
            SpacyNLSingleton.instance = SpacyNLSingleton.__SPacySingleton()
        return SpacyNLSingleton.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

    def give_tagged_speech_table(self, speech):
        doc = self.instance.val(speech)
        table = "\n\nTEXT | LEMMA | POS | TAG | DEP | SHAPE | ALPHA \n" \
                 "| ------------- |------------- | ------------- | ------------- " \
                 "| ------------- | ------------- | ------------- |\n"

        for token in doc:
            table += token.text + " | " + token.lemma_ + " | " + token.pos_ + " | " + re.sub("\|", "&#124;", token.tag_) + " | " + token.dep_ + " | " + token.shape_ + " | " + ("TRUE" if token.is_alpha else "FALSE") + " |\n"

        return table
