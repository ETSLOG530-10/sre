#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script is used to create a JSON file containing each modified files,
the author of each modification and the date of the modification.
"""

import json
import csv

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
                        modified_files[filename] = [filename, 1]
                    modified_files[filename][1] += 1

    return modified_files

def main():
    """
    Main function.
    """

    filename = input("File: ")

    # Import data form json file
    modified_files = import_data(filename)
    modified_files_list = [val for key, val in modified_files.items()]
    modified_files_list.sort(key=lambda x: x[1], reverse=True)

    # Create CSV file
    fileOutput = filename+'_touches_sorted.csv'
    rows = ["Filename", "Touches"]
    with open(fileOutput, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(rows)
        for row in modified_files_list:
            writer.writerow(row)
    

if __name__ == "__main__":
    main()
