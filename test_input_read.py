import sys
from unittest import mock
from input_read import input_read

# Expected values for testing
expected_input_files = ['test_file.txt', 'test_file1.txt', 'vaher-names-in.txt', 'vaher-flagtype1-in.txt']
expected_flags =  ['names', 'dates', 'phones', 'address']
expected_concepts = ['kids']
expected_stats = ['stderr']

# Mock sys.argv to simulate passing arguments from the command line
@mock.patch('glob.glob')
def test_input_read(mock_glob):
    # Simulate the glob result
    mock_glob.return_value = expected_input_files
    
    # Mock sys.argv to simulate passing arguments
    test_argv = [
        "script_name.py", "--input", "*.txt", "--concept", "kids", 
        "--output", "output_path", "--stats", "stderr", 
        "--names", "--dates", "--phones", "--address"
    ]

    with mock.patch.object(sys, 'argv', test_argv):
        # Call the function and capture the output
        received_input_files, received_flags, received_concepts, received_stats = input_read()

        # Perform assertions
        assert received_input_files == expected_input_files
        assert received_flags == expected_flags
        assert received_concepts == expected_concepts
        assert received_stats == expected_stats
