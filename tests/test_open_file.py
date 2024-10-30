import pytest
from unittest import mock
from open_file import open_file_in_same_directory  # Replace 'your_module' with the actual module name

# Test for open_file_in_same_directory
@mock.patch('builtins.open', new_callable=mock.mock_open, read_data="This is    a test    file.")
@mock.patch('os.path.abspath')
@mock.patch('os.path.dirname')
def test_open_file_in_same_directory(mock_dirname, mock_abspath, mock_open):
    # Mock the directory and file paths
    mock_dirname.return_value = '/fake/directory'
    mock_abspath.return_value = '/fake/directory/fake_file.txt'

    # Call the function with a mock file
    result = open_file_in_same_directory('fake_file.txt')

    # Verify the file path is constructed correctly
    mock_dirname.assert_called_once()
    mock_abspath.assert_called_once()

    # Verify that the file was opened correctly
    mock_open.assert_called_once_with('/fake/directory/fake_file.txt', 'r')

    # Expected content after splitting and joining words
    expected_content = "This is a test file."

    # Check if the result matches the expected content
    assert result == expected_content, f"Expected '{expected_content}', but got '{result}'"
