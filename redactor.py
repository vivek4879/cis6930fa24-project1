import spacy
from createdb import createdb 
import sqlite3
from names import names
from redactor12 import redact_from_db
from phone_numbers import numbers
from dates import dates
from address import address
from input_read import input_read
from concept import find_concept
import os


db_path,con = createdb()
cur = con.cursor()
input_files, flags,concepts,stats_, output_path_list= input_read()
output_ = output_path_list[0]
stats_file_name = stats_[0]
# Create output folder if it doesn't exist
if not os.path.exists(output_):
    os.makedirs(output_)
    print(f"Output directory '{output_}' created.")
else:
    print(f"Output directory '{output_}' already exists.")
redaction_dict = {}
for file in input_files:
    if len(flags) > 0:
        for flag in flags:
            if flag == 'names':
                names(cur,file,redaction_dict)
            if flag == 'dates':
                dates(cur,file,redaction_dict)
            if flag == 'phones':
                numbers(cur,file,redaction_dict)
            if flag == 'address':
                address(cur,file,redaction_dict)
    if len(concepts) > 0:
        for concept in concepts:
            find_concept(cur,file, concept, redaction_dict,threshold=0.6)

redact_from_db(cur, output_, stats_file_name,redaction_dict)
con.commit()
cur.close()



