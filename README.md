# README

## Project: The Redactor

**Course**: CIS 6930, Fall 2024  
**Project**: Project 1  
**Author**: **Vivek Milind Aher**
**Email**: vaher@ufl.edu 

---

### Overview

This project is designed to redact sensitive information (e.g., names, phone numbers, addresses, dates, and concepts) from plain text documents. It uses a command-line interface (CLI) for users to specify input files and what type of information should be redacted. The program generates new files with `.censored` appended to their names, storing them in the output directory specified by the user. It also writes a detailed summary of the redaction process to a file or to `stderr`/`stdout`.

### How to Run the Program

To run the program, use the following command:

```bash
pipenv run python redactor.py --input '*.txt' \
                              --names --dates --phones --address \
                              --concept 'kids' \
                              --output 'files/' \
                              --stats stderr
```

### Requirements
1. To set up the environment, follow these steps:

Install dependencies using Pipenv:
```bash
pipenv install
```

2. Run the program using the command structure provided above.
### File Structure
The project structure is as follows:
```bash
cis6930fa24-project1/
├── COLLABORATORS
├── LICENSE
├── README.md
├── Pipfile
├── docs/
├── redactor.py
├── setup.cfg
├── setup.py
└── tests/
    ├── test_names.py
    ├── test_phones.py
    ├── test_address.py
    ├── test_concepts.py
    └── ...
```
### Detailed Parameter Explanations
--input: Accepts a glob pattern representing input files. Supports multiple file types.
--output: Specifies the directory to store censored files. The output files have the same name as the original, with .censored appended.
Censor Flags:
--names: Censors all types of names. SpaCy's named entity recognition (NER) is used to detect proper names.
--dates: Censors all types of dates, detected using SpaCy's date recognition.
--phones: Censors phone numbers in formats such as (123) 456-7890, 123.456.7890, +1-800-555-1212, etc.
--address: Censors postal addresses using custom regex patterns.
--concept: Censors sentences containing words or ideas related to the given concept using SpaCy's word vector similarity.
--stats: Outputs statistics about the redaction process, including the types and counts of redacted items, as well as their start and end indices.


### Redaction Details
The redacted text replaces the sensitive information with a block character (U+2588) or a similar symbol of your choice. The following information is redacted:

Names: Detected using SpaCy's named entity recognition.
Dates: Detected using regular expressions and SpaCy's date recognition.
Phone Numbers: Detected using a combination of regular expressions.
Addresses: Detected using regex patterns for common address structures.
Concepts: Sentences with words or themes related to the given concept are redacted using SpaCy's word vector similarity.
Whitespace between censored words is redacted by default, but this can be customized if needed.


### Redaction Statistics
The --stats flag allows for outputting statistics related to the redaction process. The following information is captured in the stats:

Types of Redacted Items: A count of each type of redaction (names, dates, phone numbers, addresses, concepts).
Details of Redacted Items: Includes the redacted term, the type, and the start and end indices of the redacted term within the text.

The redaction stats and details are written either to a file, stderr, or stdout depending on the type given in the input. If the input says stderr or stdout then we print it to the terminal and if it says anything else then we make a .txt file of that name in our stats folder and write the stats in that file.

### Tests
Tests for each feature are provided in the tests/ directory. To run all tests, use:

```bash
pipenv run python -m pytest
```
This will execute all the test files (e.g., test_names.py, test_phones.py) and ensure that the redaction system works as expected.

### Assumptions
Names are assumed to follow typical Western name conventions, detected via SpaCy's PERSON entity.
Postal addresses are detected using common patterns and may not cover all edge cases.
Concepts are semantically detected using word embeddings provided by SpaCy's medium or large models (en_core_web_md or en_core_web_lg).


### Setup and Installation
Follow these steps to install the project:

1.Clone the repository:
```bash
git clone https://github.com/yourusername/cis6930fa24-project1.git
cd cis6930fa24-project1

```
2.Install dependencies using Pipenv:
```bash
pipenv install
```
3. To test the redaction system, run:
```bash
pipenv run python redactor.py --input '*.txt' --names --dates --phones --output 'files/' --stats stderr

```

### Functions

## Function: `redact_text(text, redactions)`

This function performs the core redaction by replacing sensitive text within the specified indices with a redaction character (█). The function sorts the redaction indices in reverse order to ensure that each redaction does not shift the indices of others.

- **Parameters**:
  - `text (str)`: The original text where redactions will be applied.
  - `redactions (list of tuples)`: A list of (start_index, end_index) tuples representing the ranges to redact.

---

## Function: `write_stats_to_file(stats_folder_path, stats_file_name, redaction_stats, redaction_dict)`

This function writes the redaction statistics and details into a file located in the specified `stats_folder_path`. It records the total number of redacted characters for each file and detailed information about each redaction (like entity, start, and end positions).

- **Parameters**:
  - `stats_folder_path`: Directory where the stats file will be saved.
  - `stats_file_name`: Name of the stats file.
  - `redaction_stats`: Dictionary storing the total number of redacted characters for each file.
  - `redaction_dict`: Dictionary storing detailed information about each redaction.

---

## Function: `redact_from_db(cur, output_path, stats_file_name, redaction_dict)`

This function processes redactions from the database and applies them to files. It fetches redaction data (file name, start, and end indices) from the database, processes the corresponding files, and performs the redactions. It also creates an output directory if it doesn't exist and ensures redacted files are saved with a .censored extension. Additionally, it writes the redaction statistics into a stats file.

- **Parameters**:
  - `cur`: Database cursor used to fetch redaction data.
  - `output_path`: Path to the folder where the redacted files will be stored.
  - `stats_file_name`: Name of the file where redaction stats will be saved.
  - `redaction_dict`: Dictionary storing detailed information about each redaction.

---

### Key Points:
- **Redaction Process**: Applies redactions to specific portions of text within files and saves the redacted versions.
- **Statistics**: Tracks the total number of characters redacted and detailed information about each redaction.
- **File Management**: Handles file reading, copying, and saving with redactions in the specified output folder.
---

## Function: `numbers(cur, file_name, redaction_dict)`

This function scans a file for phone numbers using a regular expression, validates them, and performs redactions by inserting the detected phone numbers into the database and updating a redaction dictionary.

- **Parameters**:
  - `cur`: The database cursor used to insert redacted data.
  - `file_name`: The name of the file being processed.
  - `redaction_dict`: A dictionary that tracks redaction details, including the redacted phone numbers, their positions, and labels.

- **Process**:
  1. Reads the file content using the `open_file_in_same_directory()` function.
  2. Uses a regex pattern to identify phone numbers within the text.
  3. For each valid phone number (using `valid_phone_number()`):
     - Inserts redaction details (start and end indices) into the database.
     - Updates the `redaction_dict` with information about the redacted phone numbers (entity, label, start, end).

---

## Function: `valid_phone_number(match)`

This helper function validates a matched phone number by ensuring it contains between 10 and 11 digits. It strips out non-numeric characters (such as spaces, dashes, and dots) and checks the digit count.

- **Parameters**:
  - `match`: The regex match object containing the phone number.

- **Returns**:
  - `True` if the phone number contains between 10 and 11 digits; otherwise, `False`.

---

### Key Points:
- **Phone Number Redaction**: The `numbers()` function scans and redacts valid phone numbers, inserting them into the database and updating the redaction dictionary.
- **Validation**: The `valid_phone_number()` function ensures that only valid phone numbers (with 10 or 11 digits) are processed.

---

## Function: `open_file_in_same_directory(file_name)`

This function reads the content of a file located in the same directory as the script, removes extra spaces, and returns the cleaned text.

- **Parameters**:
  - `file_name`: The name of the file to be opened.

- **Process**:
  1. Determines the directory where the script is located using `os.path.dirname(os.path.abspath(__file__))`.
  2. Builds the full file path by joining the script's directory and the file name.
  3. Opens the file in read mode, splits the content into words (to remove extra spaces between words), and then rejoins the words into a single string.
  4. Returns the cleaned file content as a string.

### Key Points:
- **File Handling**: Reads a file in the same directory as the script.
- **Whitespace Handling**: Splits and rejoins words to ensure that excessive spaces are removed from the content.

---
## Function: `input_read()`

This function reads and parses command-line arguments to extract input file patterns, flags, concepts, output paths, and stats options. It uses `sys.argv` to access the arguments and processes them accordingly.

- **Returns**: A tuple containing:
  - `input_files`: A list of files matching the provided pattern (using `glob`).
  - `flags`: A list of flags passed as command-line arguments (e.g., `--names`, `--dates`).
  - `concepts`: A list of specific concepts to be used (if any).
  - `stats_`: A list containing stats options (e.g., `stderr` or file names for stats).
  - `output_path_list`: A list of output paths where redacted files should be stored.

- **Process**:
  1. Loops through the command-line arguments (`sys.argv`).
  2. Identifies and captures arguments for:
     - `--input`: File pattern (e.g., `*.txt`).
     - `--concept`: Concepts to use in the redaction process.
     - `--output`: Output directory for saving redacted files.
     - `--stats`: File or destination for saving redaction statistics.
     - Other flags (e.g., `--names`, `--dates`), which are stored in `flags`.
  3. Uses `glob.glob()` to find files matching the input pattern.
  4. Returns the parsed input, flags, and paths.

### Key Points:
- **Command-Line Parsing**: Reads and interprets arguments from the command line.
- **File Pattern Matching**: Uses `glob` to match input files based on the pattern provided via `--input`.
- **Flexible Arguments**: Supports multiple types of input including flags, concepts, and output paths.

---

