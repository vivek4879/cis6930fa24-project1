import re
import spacy
from open_file import open_file_in_same_directory

def dates(cur, file_name, redaction_dict):
    # Read the content of the file
    text = open_file_in_same_directory(file_name)

    # Load a larger model to improve accuracy, if available
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)

    # Initialize the file entry in the dictionary if it doesn't exist
    if file_name not in redaction_dict:
        redaction_dict[file_name] = {}

    # Loop over the named entities and check for dates
    for ent in doc.ents:
        # Filter out entities that are purely numeric and too long to be a realistic date
        if ent.label_ == "DATE" and not re.fullmatch(r"\d{5,}", ent.text):
            start_ = ent.start_char
            end_ = ent.end_char

            # Insert date redactions into the database
            insertion_query = "INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)"
            cur.execute(insertion_query, (file_name, start_, end_))

            # Add the date redaction details to the redaction_dict
            if "DATE" not in redaction_dict[file_name]:
                redaction_dict[file_name]["DATE"] = []

            redaction_dict[file_name]["DATE"].append({
                'entity': ent.text,
                'label': "DATE",
                'start': start_,
                'end': end_
            })

    return redaction_dict
