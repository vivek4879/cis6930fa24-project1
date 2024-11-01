from open_file import open_file_in_same_directory
import spacy
import sqlite3

def names(cur, file_name, redaction_dict):
    text = open_file_in_same_directory(file_name)
    # Load the small English language model
    nlp = spacy.load("en_core_web_lg")

    doc = nlp(''.join(text))

    # Initialize an empty dictionary for the file if it doesn't exist
    if file_name not in redaction_dict:
        redaction_dict[file_name] = {}

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            start_ = ent.start_char
            end_ = ent.end_char
            # print(ent, ent.label_, start_, end_)

            # Insert the redaction into the database
            insertion_query = "INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)"
            cur.execute(insertion_query, (file_name, start_, end_))

            # Add the redaction details to the dictionary
            if ent.label_ not in redaction_dict[file_name]:
                redaction_dict[file_name][ent.label_] = []
            
            redaction_dict[file_name][ent.label_].append({
                'entity': ent.text,
                'label': ent.label_,
                'start': start_,
                'end': end_
            })

    return redaction_dict
