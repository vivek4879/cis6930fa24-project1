
from open_file import open_file_in_same_directory
import spacy

def dates(cur, file_name):
    # file_name = "vaher-names1-in"
    text = open_file_in_same_directory(file_name)
    print(text)
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(''.join(text))

    for ent in doc.ents:
        if ent.label_ == "DATE":
            start_ = ent.start_char
            end_ = ent.end_char
            print(ent, ent.label_, start_, end_)
            insertion_query = "INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)"
            cur.execute(insertion_query, (file_name,start_, end_))




   