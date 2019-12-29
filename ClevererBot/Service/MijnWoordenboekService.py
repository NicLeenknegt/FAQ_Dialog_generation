from ClevererBot.Service.BaseService import BaseService
from ClevererBot.Utils.JsonReader import JsonReader
from ClevererBot.Domain.Enum.ThesaurusWordTypeEnum import ThesaurusWordType
import json
import re
from ClevererBot.Domain.Enum.RegexPatterns import RegexPatterns

class MijnWoordenboekService:

    def __init__(self):
        self.base_service = BaseService()
        self.json_reader = JsonReader()

    @BaseService.send_url_request("https://www.mijnwoordenboek.nl/synoniem.php?woord={}&lang=NL")
    def get_synonym_html(self, word):
        return word

    def html_to_list(self, word):
        res = []
        html = re.findall(RegexPatterns.SYNONYMS_FROM_MIJN_WOORDENBOEK.value, self.get_synonym_html(word).decode(), re.DOTALL)
        if html:
            for a in re.findall(RegexPatterns.A_HTML_PATTERN_MINIMAL.value, html[0]):
                res.append(re.sub(RegexPatterns.HTML_ELEMENT_PATTERN_MINIMAL.value, "", a))
        return res

    def get_synonym_list(self,word):
        return self.html_to_list(word)