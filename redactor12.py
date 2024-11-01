import sqlite3
import os
from collections import defaultdict

def redact_text(text, redactions):
    """
    Apply multiple redactions to the text based on start and end indices.
    Args:
    - text (str): The input text to redact.
    - redactions (list of tuples): List of (start_index, end_index) for redactions.
    Returns:
    - str: Redacted text.
    """
    # Sort redactions in reverse order to avoid affecting subsequent indices
    redactions = sorted(redactions, key=lambda x: x[0], reverse=True)
    for start_index, end_index in redactions:
        chars_to_redact = end_index - start_index
        text = text[:start_index] + ('█' * chars_to_redact) + text[end_index:]
    return text

def redact_from_db(cur, output_path, stats_file_name, redaction_dict):
    try:
        # Fetch all rows and group them by file name
        cur.execute("SELECT File_name, start_index, end_index FROM redactions")
        rows = cur.fetchall()

        # Group rows by file name
        redactions_by_file = defaultdict(list)
        for row in rows:
            file_name = row[0]
            start_index = row[1]
            end_index = row[2]
            redactions_by_file[file_name].append((start_index, end_index))

        # Dictionary to store total redacted characters for each file
        redaction_stats = defaultdict(int)

        for file_name, redactions in redactions_by_file.items():
            # Read the original file
            input_file_path = os.path.join('.', file_name)
            if not os.path.exists(input_file_path):
                print(f"Original file not found: {input_file_path}")
                continue

            with open(input_file_path, 'r') as file:
                text_ = file.read()
                words_ = text_.split()
                text = ' '.join(words_)

            # Apply all redactions in one go
            redacted_text = redact_text(text, redactions)
            total_redacted_chars = sum(end - start for start, end in redactions)
            redaction_stats[file_name] += total_redacted_chars

            # Write the redacted text to a new file with .censored extension
            base_name, _ = os.path.splitext(file_name)
            output_file_name = base_name + ".censored"
            output_file_path = os.path.join(output_path, output_file_name)
            with open(output_file_path, 'w') as file:
                file.write(redacted_text)
            print(f"Redacted file created: {output_file_path}")

        # Create 'stats' folder in the root project directory
        stats_folder_path = os.path.join(os.getcwd(), "stats")
        if not os.path.exists(stats_folder_path):
            os.makedirs(stats_folder_path)
            print(f"'Stats' directory created at: {stats_folder_path}")

        # Write stats to file
        write_stats_to_file(stats_folder_path, stats_file_name, redaction_stats, redaction_dict)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def write_stats_to_file(stats_folder_path, stats_file_name, redaction_stats, redaction_dict):
    """
    Writes redaction stats and details to a file.
    
    Args:
    - stats_folder_path: The folder path where the stats file should be saved.
    - stats_file_name: The name of the stats file.
    - redaction_stats: Dictionary storing the total number of redacted characters per file.
    - redaction_dict: Dictionary storing the detailed redaction information.
    """
    stats_file_path = os.path.join(stats_folder_path, stats_file_name)
    with open(stats_file_path, "w") as stats_file:
        for file_name, total_redacted_chars in redaction_stats.items():
            stats_file.write(f"{file_name}: {total_redacted_chars} characters redacted\n")
            
            if file_name in redaction_dict:
                stats_file.write(f"Details of redactions in {file_name}:\n")
                for redaction_type, redactions in redaction_dict[file_name].items():
                    stats_file.write(f"  Redaction Type: {redaction_type}\n")
                    for redaction in redactions:
                        entity = redaction.get('entity', 'Unknown')
                        start = redaction.get('start', 'Unknown')
                        end = redaction.get('end', 'Unknown')
                        stats_file.write(f"    Entity: {entity}, Start: {start}, End: {end}\n")
            else:
                stats_file.write(f"No redaction details found for {file_name}.\n")

    print(f"Redaction stats saved to: {stats_file_path}")
