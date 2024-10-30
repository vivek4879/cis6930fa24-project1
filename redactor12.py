import sqlite3
import os
import shutil
from collections import defaultdict

def redact(file_path, start_index, end_index):
    try:
        with open(file_path, 'r') as file:
            text_ = file.read()
            words_ = text_.split()
            text = ' '.join(words_)

        chars_to_redact = end_index - start_index

        redacted_text = text[:start_index] + ('█' * chars_to_redact) + text[end_index:]

        with open(file_path, 'w') as file:
            file.write(redacted_text)
    except Exception as e:
        print(f"Error redacting file {file_path}: {e}")

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
            # Write the total redacted characters for each file
            stats_file.write(f"{file_name}: {total_redacted_chars} characters redacted\n")
            
            # Write redaction dictionary contents for each file
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

def redact_from_db(cur, output_path, stats_file_name, redaction_dict):
    try:
        # Fetch all rows from the 'redactions' table
        cur.execute("SELECT File_name, start_index, end_index FROM redactions")
        rows = cur.fetchall()

        # Dictionary to store total redacted characters for each file
        redaction_stats = defaultdict(int)

        for row in rows:
            file_name = row[0]
            start_index = row[1]
            end_index = row[2]

            # Calculate number of characters redacted in this operation
            redacted_chars = end_index - start_index
            redaction_stats[file_name] += redacted_chars

            # Ensure the output file has a .txt extension
            base_name, _ = os.path.splitext(file_name)  # Get file name without extension
            output_file_name = base_name + ".txt"       # Create .txt file name

            # Build the file path for both the input and the output
            input_file_path = os.path.join('.', file_name)  # Original file location
            output_file_path = os.path.join(output_path, output_file_name)  # File in output folder with .txt extension

            # Check if the output folder exists, if not create it
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                print(f"Output directory '{output_path}' created.")

            # Check if the file already exists in the output directory
            if os.path.exists(output_file_path):
                print(f"Using file from output directory: {output_file_path}")
                # If the file exists in the output path, redact the existing output file
                redact(output_file_path, start_index, end_index)
            else:
                if os.path.exists(input_file_path):
                    print(f"Processing original file: {input_file_path}")
                    # Copy the original file to the output directory with the .txt extension
                    shutil.copy(input_file_path, output_file_path)
                    print(f"File copied to: {output_file_path}")
                    # Perform the redaction on the newly copied file
                    redact(output_file_path, start_index, end_index)
                else:
                    print(f"Original file not found: {input_file_path}")

        # Create 'stats' folder in the root project directory
        root_directory = os.getcwd()  # Get the current working directory (root directory)
        stats_folder_path = os.path.join(root_directory, "stats")
        if not os.path.exists(stats_folder_path):
            os.makedirs(stats_folder_path)
            print(f"'Stats' directory created at: {stats_folder_path}")
        else:
            print(f"'Stats' directory already exists.")

        # Write stats to file by calling the new function
        write_stats_to_file(stats_folder_path, stats_file_name, redaction_stats, redaction_dict)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
