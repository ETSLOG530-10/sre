#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script is used to create a JSON file containing each modified files,
the author of each modification and the date of the modification.
"""

import json

def import_data(filename):
    """
    Import data from json file.
    """
    modified_files = {}
    with open('rootbeer.json', 'r') as f:
        data = json.load(f)
        for line in data:
            commit = line['commit']
            files = line['files']
            author = commit['author']
            for file in files:
                filename = file['filename']
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

    # Import data form json file
    modified_files = import_data('rootbeer.json')

    # Display data
    display_data(modified_files)
    

if __name__ == "__main__":
    main()


