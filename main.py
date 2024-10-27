import spacy
from createdb import createdb 
import sqlite3
from names import names
from redactor import redact_from_db
from phone_numbers import numbers
from dates import dates
from address import address
from input_read import input_read

db_path,con = createdb()
cur = con.cursor()
input_files, flags,concepts,stats_ = input_read()
print(input_files)
for file in input_files:
    if len(flags) > 0:
        for flag in flags:
            if flag == 'names':
                names(cur,file)
            if flag == 'dates':
                dates(cur,file)
            if flag == 'phones':
                numbers(cur,file)
            if flag == 'address':
                address(cur,file)
    # if len(concepts) > 0:
    #     for concept in concepts:
    #         concept(cur,file)

redact_from_db(cur)
con.commit()
cur.close()


