import pytest
from unittest import mock
import spacy
from names import names  

# Mocked content of the file to simulate the open_file function
mocked_file_content = "John Doe is the CEO of ExampleCorp. Jane Smith works there as well."

# Mock Spacy output for the file content
@pytest.fixture
def spacy_nlp():
    # Initialize Spacy model for testing
    return spacy.load("en_core_web_sm")

# Test for the 'names' function
@mock.patch('names.open_file_in_same_directory')  
def test_names(mock_open_file, spacy_nlp):
    # Mock the file reading function to return our mocked content
    mock_open_file.return_value = mocked_file_content

    # Create a mock database cursor
    mock_cur = mock.Mock()

    # Initialize the redaction dictionary
    redaction_dict = {}

    # Call the 'names' function
    file_name = 'test_file.txt'
    names(mock_cur, file_name, redaction_dict)

    # Assertions to ensure correct SQL insertion is called
    # Spacy should detect "John Doe" and "Jane Smith" as PERSON entities
    expected_sql_calls = [
        mock.call("INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)",
                  (file_name, 0, 8)),   # "John Doe"
        mock.call("INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)",
                  (file_name, 36, 46))  # "Jane Smith"
    ]

    # Check that cur.execute was called with the correct arguments
    mock_cur.execute.assert_has_calls(expected_sql_calls, any_order=True)

    # Ensure it was called twice (once for each detected PERSON)
    assert mock_cur.execute.call_count == 2

    # Verify the redaction_dict contains the correct entries
    expected_redaction_dict = {
        file_name: {
            "PERSON": [
                {'entity': "John Doe", 'label': "PERSON", 'start': 0, 'end': 8},
                {'entity': "Jane Smith", 'label': "PERSON", 'start': 36, 'end': 46}
            ]
        }
    }

    # Check the redaction_dict contains the correct redactions
    assert redaction_dict == expected_redaction_dict, f"Expected {expected_redaction_dict}, but got {redaction_dict}"
