import spacy
import os
import sqlite3

    

def open_file_in_same_directory(file_name):
   script_dir = os.path.dirname(os.path.abspath(__file__))
   file_path = os.path.join(script_dir, file_name)

   with open(file_path, 'r') as file:
    #   content = file.readlines()
      text = file.read()
      words = text.split()
      content = ' '.join(words)

   return content

