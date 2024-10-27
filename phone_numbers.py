import re
from open_file import open_file_in_same_directory
def numbers(cur,file_name):
    # file_name = "vaher-names1-in"
    text = open_file_in_same_directory(file_name)
    phoneNumRegex = re.compile(r'''
    (?:\+?\d{1,3}[-.\s]?)?         
    \(?\d{2,4}\)?[-.\s]?           
    \d{3}[-.\s]?                  
    \d{3,4}                       
    (?:[-.\s]\d{3,4})?
    (?!\d)            
''', re.VERBOSE)
    matches = phoneNumRegex.finditer(text)

    for match in matches:
    # Use the helper function to validate the length
        if valid_phone_number(match):
            # Insert valid phone numbers into the database
            insertion_query = "INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)"
            cur.execute(insertion_query, (file_name, match.start(), match.end()))
            print(f"Found phone number: {match.group()} at index {match.start()} to {match.end()}")

# Helper function to count digits in a phone number and ensure it has 10 or 11 digits
def valid_phone_number(match):
    # Remove separators (spaces, dashes, dots)
    phone_number = re.sub(r'[-.\s]', '', match.group())
    # Ensure total digits are between 10 and 11
    return 10 <= len(phone_number) <= 11



