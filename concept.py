from open_file import open_file_in_same_directory
import spacy

def find_concept(cur, file_name, concept, redaction_dict, threshold=0.6):
    # Read the content of the file
    text = open_file_in_same_directory(file_name)

    # Load the large English language model for named entity recognition and similarity checks
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(''.join(text))
    concept_lower = concept.lower()  # Lowercase the concept for matching
    concept_doc = nlp(concept)  # Process the concept with SpaCy for similarity checks

    # Initialize the file entry in the dictionary if it doesn't exist
    if file_name not in redaction_dict:
        redaction_dict[file_name] = {}

    # Loop over each sentence in the document
    for sentence in doc.sents:
        sentence_text_lower = sentence.text.lower()

        sentence_contains_concept = False  # Track whether the sentence contains the concept

        # Check if the concept word/phrase is directly in the sentence or part of a token
        for token in sentence:
            token_lemma = token.lemma_.lower()  # Lemma of the token

            # Match concept if it is part of the token or its lemma
            if concept_lower in token.text.lower() or concept_lower in token_lemma:
                sentence_contains_concept = True
                break

        # Redact if the concept is found in the sentence
        if sentence_contains_concept:
            start_ = sentence.start_char
            end_ = sentence.end_char
            # print(f"Redacting sentence (exact match): {sentence.text.strip()} (Start: {start_}, End: {end_})")

            # Insert the redaction into the database
            insertion_query = "INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)"
            cur.execute(insertion_query, (file_name, start_, end_))

            # Add the concept redaction details to the redaction_dict
            if "CONCEPT" not in redaction_dict[file_name]:
                redaction_dict[file_name]["CONCEPT"] = []

            redaction_dict[file_name]["CONCEPT"].append({
                'entity': sentence.text.strip(),
                'label': "CONCEPT",
                'start': start_,
                'end': end_
            })

        # If no direct match is found, check similarity
        else:
            similarity = concept_doc.similarity(sentence)
            if similarity > threshold:
                start_ = sentence.start_char
                end_ = sentence.end_char
                # print(f"Redacting sentence (similarity: {similarity:.2f}): {sentence.text.strip()} (Start: {start_}, End: {end_})")

                # Insert the redaction into the database
                insertion_query = "INSERT INTO redactions(File_name, start_index, end_index) VALUES (?,?,?)"
                cur.execute(insertion_query, (file_name, start_, end_))

                # Add the redaction details to the redaction_dict
                if "CONCEPT" not in redaction_dict[file_name]:
                    redaction_dict[file_name]["CONCEPT"] = []

                redaction_dict[file_name]["CONCEPT"].append({
                    'entity': sentence.text.strip(),
                    'label': "CONCEPT",
                    'start': start_,
                    'end': end_
                })

    return redaction_dict
