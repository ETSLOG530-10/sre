#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script is used to create a JSON file containing each modified files,
the author of each modification and the date of the modification.
"""

import json
import csv
import CollectFiles

code_exts = [".kt", ".java", ".cpp", ".h", ".js", ".scss", ".css"]
def is_code_file(filename):
    for code_ext in code_exts:
        if filename.endswith(code_ext):
            return True
    return False

def import_data(filename):
    """
    Import data from json file.
    """
    modified_files = {}
    with open(filename, 'r') as f:
        data = json.load(f)
        for line in data:
            commit = line['commit']
            files = line['files']
            author = commit['author']
            for file in files:
                filename = file['filename']
                if filename.startswith('app/src') and is_code_file(filename):
                    if filename not in modified_files:
                        modified_files[filename] = []
                    modified_files[filename].append((author['name'], author['date']))

    return modified_files

def display_data(modified_files):
    for filename, modifications in modified_files.items():
        print("--------------------------")
        print("File: {}".format(filename))
        print("Modifications:")
        print("\n".join(["\t{} - {}".format(author, date) for author, date in modifications]))

def main():
    """
    Main function.
    """

    filename = input("File: ")

    # Import data form json file
    modified_files = import_data(filename)

    # Display data
    display_data(modified_files)

    # export data to json file
    with open(f'{filename}_sorted.json', 'w') as f:
        json.dump(modified_files, f)
    

if __name__ == "__main__":
    main()


