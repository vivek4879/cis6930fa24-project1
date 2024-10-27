import sqlite3
import os

def redact(file_path, start_index, end_index):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            words = text.split()
            content = ' '.join(words)

        chars_to_redact = end_index - start_index

        redacted_text = content[:start_index] + ('█' * chars_to_redact) + content[end_index:]

        with open(file_path, 'w') as file:
            file.write(redacted_text)
    except Exception as e:
        print(f"Error redacting file {file_path}: {e}")

def redact_from_db(cur):
    try:
        # Connect to the database
        # con = sqlite3.connect(db_path)
        # cur = con.cursor()

        # Fetch all rows from the 'redactions' table
        cur.execute("SELECT File_name, start_index, end_index FROM redactions")
        rows = cur.fetchall()

        for row in rows:
            file_name = row[0]
            start_index = row[1]
            end_index = row[2]

            # Build the full file path if necessary (depends on your directory structure)
            file_path = os.path.join('.', file_name)  # Adjust the path as needed

            if os.path.exists(file_path):
                print(f"Processing file: {file_path} | Start index: {start_index}, End index: {end_index}")
                redact(file_path, start_index, end_index)
            else:
                print(f"File not found: {file_path}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")