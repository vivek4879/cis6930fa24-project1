import sys
import os
from unittest import mock
from input_read import input_read
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Expected values for testing
expected_input_files = ['test_file.txt', 'test_file1.txt', 'vaher-names-in.txt', 'vaher-flagtype1-in.txt']
expected_flags = ['names', 'dates', 'phones', 'address']
expected_concepts = ['kids']
expected_stats = ['stderr']
expected_output_path = ['output_path'] # Assuming output_path is now returned by input_read

# Mock sys.argv to simulate passing arguments from the command line
@mock.patch('glob.glob')  # Mock glob for file pattern matching
def test_input_read(mock_glob):
    # Simulate the glob result
    mock_glob.return_value = expected_input_files
    
    # Mock sys.argv to simulate passing arguments
    test_argv = [
        "script_name.py", "--input", "*.txt", "--concept", "kids", 
        "--output", "output_path", "--stats", "stderr", 
        "--names", "--dates", "--phones", "--address"
    ]

    # Mock sys.argv to simulate the command-line arguments
    with mock.patch.object(sys, 'argv', test_argv):
        # Call the function and capture the output
        received_input_files, received_flags, received_concepts, received_stats, received_output_path = input_read()

        # Perform assertions
        assert received_input_files == expected_input_files, f"Expected {expected_input_files}, got {received_input_files}"
        assert received_flags == expected_flags, f"Expected {expected_flags}, got {received_flags}"
        assert received_concepts == expected_concepts, f"Expected {expected_concepts}, got {received_concepts}"
        assert received_stats == expected_stats, f"Expected {expected_stats}, got {received_stats}"
        assert received_output_path == expected_output_path, f"Expected {expected_output_path}, got {received_output_path}"
