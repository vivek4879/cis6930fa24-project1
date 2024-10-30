import re
from open_file import open_file_in_same_directory

def numbers(cur, file_name, redaction_dict):
    # Read the content of the file
    text = open_file_in_same_directory(file_name)

    # Define the regex pattern for phone numbers
    phoneNumRegex = re.compile(r'''
    (?:\+?\d{1,3}[-.\s]?)?       # Optional country code
    \(?\d{2,4}\)?[-.\s]?         # Area code (with optional parentheses)
    \d{3}[-.\s]?                 # First part of the number
    \d{3,4}                      # Second part of the number
    (?:[-.\s]\d{3,4})?           # Optional extension or additional part
    (?!\d)                       # Ensure no more digits follow
    ''', re.VERBOSE)

    matches = phoneNumRegex.finditer(text)

    # Initialize the file entry in the dictionary if it doesn't exist
    if file_name not in redaction_dict:
        redaction_dict[file_name] = {}

    for match in matches:
        # Use the helper function to validate the phone number length
        if valid_phone_number(match):
            # Insert valid phone numbers into the database
            insertion_query = "INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)"
            cur.execute(insertion_query, (file_name, match.start(), match.end()))

            # Add the redaction details to the dictionary
            if "PHONE" not in redaction_dict[file_name]:
                redaction_dict[file_name]["PHONE"] = []

            redaction_dict[file_name]["PHONE"].append({
                'entity': match.group(),
                'label': "PHONE",
                'start': match.start(),
                'end': match.end()
            })

            # print(f"Found phone number: {match.group()} at index {match.start()} to {match.end()}")

    return redaction_dict

# Helper function to validate the length of the phone number
def valid_phone_number(match):
    # Remove separators (spaces, dashes, dots) and keep only digits
    phone_number = re.sub(r'[^0-9]', '', match.group())  # Remove all non-numeric characters
    # Ensure the phone number contains between 10 and 11 digits
    return 10 <= len(phone_number) <= 11
