import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")
doc = nlp("My name is BIll.")
matcher = Matcher(nlp.vocab)
# pattern = [{"LOWER": "good"}, {"LOWER": "morning"}, {"IS_PUNCT": True}]
pattern = [{"TEXT": "Bill"}]
matcher.add("morningGreating",[pattern])
matches = matcher(doc)
for match_id, start, end in matches:
    m_span = doc[start:end]
    print(start, end, m_span.text)