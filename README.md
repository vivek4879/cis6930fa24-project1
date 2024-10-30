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
Whitespace between censored words is not redacted by default, but this can be customized if needed.


### Redaction Statistics
The --stats flag allows for outputting statistics related to the redaction process. The following information is captured in the stats:

Types of Redacted Items: A count of each type of redaction (names, dates, phone numbers, addresses, concepts).
Details of Redacted Items: Includes the redacted term, the type, and the start and end indices of the redacted term within the text.

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

