import spacy
from spacy.matcher import Matcher
from open_file import open_file_in_same_directory

def address(cur,file_name):
    # Load the file content
    text = open_file_in_same_directory(file_name)

    # Initialize SpaCy and Matcher
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)

    # Pattern 1: Match simple street addresses (e.g., "1234 Elm Street")
    street_address_pattern = [
    {"IS_DIGIT": True},  # Match street number (e.g., 1234)
    {"IS_ALPHA": True},  # Match street name (e.g., Elm, Maple)
    {"LOWER": {"IN": ["street", "st", "avenue", "ave", "road", "rd", "boulevard", "blvd", "lane", "ln", "drive", "dr"]}}  # Match street type
]

# Pattern 2: Match complex addresses with floors, building names, and cities (e.g., "5th floor of the 600 Jefferson building in Houston")
    complex_address_pattern = [
    {"IS_DIGIT": True},                            # Floor number (e.g., 5)
    {"LOWER": {"REGEX": "(st|nd|rd|th)"}},         # Ordinal suffix (e.g., "th")
    {"LOWER": "floor"},                            # The word "floor"
    {"LOWER": {"IN": ["of", "the"]}, "OP": "?"},   # Optional "of" or "the"
    {"IS_DIGIT": True},                            # Building number (e.g., 600)
    {"IS_ALPHA": True},                            # Building name (e.g., "Jefferson")
    {"LOWER": "building"},                         # The word "building"
    {"LOWER": "in"},                               # Preposition "in"
    {"ENT_TYPE": "GPE"}                            # City name (e.g., "Houston")
]

    # Add both patterns to the matcher
    matcher.add("STREET_ADDRESS_PATTERN", [street_address_pattern])
    matcher.add("COMPLEX_ADDRESS_PATTERN", [complex_address_pattern])

    # Process the text
    doc = nlp(text)

    # Apply the matcher
    matches = matcher(doc)
    for match_id, start, end in matches:
        m_span = doc[start:end]  # Extract the matched span from the document
        # print(m_span, start, end)

        # Insertion into the database
        insertion_query = "INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)"
        cur.execute(insertion_query, (file_name, start, end))
