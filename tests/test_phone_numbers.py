import pytest
from unittest import mock
import re
from phone_numbers import numbers, valid_phone_number 

# Mocked content of the file to simulate the open_file function
mocked_file_content = """
This is some text with phone numbers.
Call me at (123) 456-7890 or 987.654.3210.
Invalid number: 12345.
Also, +1-800-555-1212 is another number.
"""

# Test for the 'numbers' function
@mock.patch('phone_numbers.open_file_in_same_directory')  # Mock the correct usage of open_file_in_same_directory
def test_numbers(mock_open_file):
    # Mock the file content to return our test data
    mock_open_file.return_value = mocked_file_content

    # Mock the database cursor
    mock_cur = mock.Mock()

    # Initialize the redaction dictionary
    redaction_dict = {}

    # Call the 'numbers' function with the mock cursor, file name, and redaction dictionary
    file_name = 'test_file.txt'
    numbers(mock_cur, file_name, redaction_dict)

    # List of valid phone numbers with expected start and end indices
    expected_phone_numbers = [
        {"number": "(123) 456-7890", "start": 50, "end": 64},
        {"number": "987.654.3210", "start": 68, "end": 80},
        {"number": "+1-800-555-1212", "start": 111, "end": 126}
    ]

    # Ensure cur.execute is called for each valid phone number
    expected_sql_calls = [
        mock.call("INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)",
                  (file_name, entry["start"], entry["end"])) for entry in expected_phone_numbers
    ]

    # Assert that the database insertions were called with the expected values
    mock_cur.execute.assert_has_calls(expected_sql_calls, any_order=True)

    # Ensure the correct number of valid phone numbers were inserted into the database
    assert mock_cur.execute.call_count == len(expected_phone_numbers)

    # Verify that the redaction dictionary was updated correctly
    expected_redaction_dict = {
        file_name: {
            "PHONE": [
                {'entity': "(123) 456-7890", 'label': "PHONE", 'start': 50, 'end': 64},
                {'entity': "987.654.3210", 'label': "PHONE", 'start': 68, 'end': 80},
                {'entity': "+1-800-555-1212", 'label': "PHONE", 'start': 111, 'end': 126}
            ]
        }
    }

    # Check that the redaction_dict contains the correct redactions
    assert redaction_dict == expected_redaction_dict, f"Expected {expected_redaction_dict}, but got {redaction_dict}"


# Test the valid_phone_number helper function
@pytest.mark.parametrize("input_number, expected", [
    ("(123) 456-7890", True),  # 10 digits
    ("987.654.3210", True),  # 10 digits
    ("+1-800-555-1212", True),  # 11 digits
    ("12345", False),  # Too short
    ("123-456-78901", False)  # Too long
])
def test_valid_phone_number(input_number, expected):
    # Use a regex to match the phone number from the input string
    phoneNumRegex = re.compile(r'''
        (?:\+?\d{1,3}[-.\s]?)?         
        \(?\d{2,4}\)?[-.\s]?           
        \d{3}[-.\s]?                  
        \d{3,4}                       
        (?:[-.\s]\d{3,4})?
        (?!\d)            
    ''', re.VERBOSE)

    match = phoneNumRegex.search(input_number)

    # Call the helper function to validate the phone number length
    if match:
        result = valid_phone_number(match)
        assert result == expected
    else:
        assert not expected
