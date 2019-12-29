from enum import Enum
class RegexPatterns(Enum):
    SYNONYMS_FROM_MIJN_WOORDENBOEK = "<h2>Synoniemen van.+<ul.+>.+</ul><h2>P"
    A_HTML_PATTERN_MINIMAL = "<a.+?>.+?</a>"
    HTML_ELEMENT_PATTERN_MINIMAL = "<.+?>"

