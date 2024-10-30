import os
import sqlite3
def createdb():
    if os.path.exists("./resources/redactdb.db"):
        os.remove("./resources/redactdb.db")
    
    db_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),'resources'))
    # print(db_directory)
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
        print("directory created")
    
    db_path = os.path.join(db_directory, 'redactdb.db')

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS redactions")
    cur.execute("CREATE TABLE IF NOT EXISTS redactions(File_name TEXT, start_index INTEGER, end_index INTEGER);")
    print("table created")
    con.commit()
    return (db_path, con)