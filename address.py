import spacy
from spacy.matcher import Matcher
from open_file import open_file_in_same_directory

def address(cur, file_name, redaction_dict):
    # Load the file content
    text = open_file_in_same_directory(file_name)

    # Initialize SpaCy and Matcher
    nlp = spacy.load("en_core_web_lg")
    matcher = Matcher(nlp.vocab)

    # Pattern 1: Match simple street addresses (e.g., "1234 Elm Street")
    street_address_pattern = [
        {"IS_DIGIT": True},  # Match street number (e.g., 1234)
        {"IS_ALPHA": True, "OP": "+"},  # Match street name, allowing multi-word names (e.g., "Elm", "Main St")
        {"LOWER": {"IN": ["street", "st", "avenue", "ave", "road", "rd", "boulevard", "blvd", "lane", "ln", "drive", "dr"]}}
    ]

    # Pattern 2: Match complex addresses with floors, building names, and cities (e.g., "5th floor of the 600 Jefferson building in Houston")
    complex_address_pattern = [
        {"IS_DIGIT": True, "OP": "?"},               # Optional floor number (e.g., "5th")
        {"LOWER": {"REGEX": "(st|nd|rd|th)"}, "OP": "?"},  # Optional ordinal suffix (e.g., "th")
        {"LOWER": "floor", "OP": "?"},               # Optional "floor"
        {"LOWER": {"IN": ["of", "the"]}, "OP": "?"}, # Optional "of" or "the"
        {"IS_DIGIT": True, "OP": "?"},               # Optional building number (e.g., 600)
        {"IS_ALPHA": True, "OP": "+"},               # Building name or additional words (e.g., "Jefferson")
        {"LOWER": {"IN": ["building", "center"]}, "OP": "?"}, # Optional "building" or "center"
        {"LOWER": "in", "OP": "?"},                  # Optional "in"
        {"ENT_TYPE": "GPE"}                          # City name (e.g., "Houston")
    ]

    # Add both patterns to the matcher
    matcher.add("STREET_ADDRESS_PATTERN", [street_address_pattern])
    matcher.add("COMPLEX_ADDRESS_PATTERN", [complex_address_pattern])

    # Process the text
    doc = nlp(text)

    # Initialize the file entry in the dictionary if it doesn't exist
    if file_name not in redaction_dict:
        redaction_dict[file_name] = {}

    # Initialize the 'ADDRESS' entry in the dictionary if it doesn't exist
    if "ADDRESS" not in redaction_dict[file_name]:
        redaction_dict[file_name]["ADDRESS"] = []

    # Apply the matcher
    matches = matcher(doc)
    for match_id, start, end in matches:
        m_span = doc[start:end]  # Extract the matched span from the document
        # print(f"Matched address: {m_span}, Start: {start}, End: {end}")

        # Insert the matched address into the database
        insertion_query = "INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)"
        cur.execute(insertion_query, (file_name, start, end))

        # Add the address redaction details to the redaction_dict
        redaction_dict[file_name]["ADDRESS"].append({
            'entity': m_span.text,
            'label': "ADDRESS",
            'start': start,
            'end': end
        })

    return redaction_dict
