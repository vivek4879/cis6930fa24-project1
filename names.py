
from open_file import open_file_in_same_directory
import spacy
import sqlite3
def names(cur,file_name):
    text = open_file_in_same_directory(file_name)
    print(text)
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(''.join(text))

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            start_ = ent.start_char
            end_ = ent.end_char
            print(ent, ent.label_, start_, end_)
            insertion_query = "INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)"
            cur.execute(insertion_query, (file_name,start_, end_))




   