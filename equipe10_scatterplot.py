#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script is used to generate a scatterplot of commits per week and per author.
"""
import matplotlib.pyplot as plt
import numpy as np
import json
from functools import reduce
import random
import datetime
from dateutil import parser

# Constants
number_of_colors = 20
colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

def import_data(filename):
    """
    Import data from json file.
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def extract_filenames(data):
    """
    Extract filenames from json data.
    """
    return list(data.keys())

def extract_authors(data):
    """
    Extract authors from json data.
    """
    # Get all modifications
    values = list(data.values())
    # Flatten into single of lists
    single_list = reduce(lambda x,y: x+y, values)
    # Flatten into single list
    single_list = reduce(lambda x,y: x+y, single_list)
    # Get only authors (even indexes)
    only_authors = single_list[::2]
    # Return unique authors
    return list(set(only_authors))

# Function to map the colors to authors
def assign_color(authors):
    authors_colored = {}
    for i in range(len(authors)):
        authors_colored[authors[i]] = colors[i]
    return authors_colored

def get_oldest_date(data):
    """
    Get the oldest date from the json data.
    """
    # Get all modifications
    values = list(data.values())
    # Flatten into single of lists
    single_list = reduce(lambda x,y: x+y, values)
    # Flatten into single list
    single_list = reduce(lambda x,y: x+y, single_list)
    # Get only dates (odd indexes)
    only_dates = single_list[1::2]
    # Get the oldest date
    oldest_date = min(only_dates)
    return oldest_date

def convert_date_to_weeks(date, first_date):
    """
    Converts a date to weeks, based on the oldest date.
    """
    # Get the difference in days
    diff = date - first_date
    # Convert to weeks
    weeks = diff.days / 7
    return weeks


def generate_scatterplot(data, filenames, authors):
    """
    Generate a scatterplot of commits per week and per author.
    """
    authors_colored=assign_color(authors)
    oldest_date = get_oldest_date(data)
    oldest_date = parser.parse(oldest_date)
    print(oldest_date)

    file_index = 0
    for file in data:
        for modif in data[file]:
            author = modif[0]
            date = parser.parse(modif[1])
            weeks = convert_date_to_weeks(date, oldest_date)
            plt.scatter(file_index, weeks, color=authors_colored[author])
        file_index += 1

    # plt.grid(True)
    plt.show()

def main():
    """
    Main function.
    """
    # Import data form json file
    data = import_data('rootbeer_sorted.json')

    filenames = extract_filenames(data)
    print(len(filenames))

    authors = extract_authors(data)
    print(authors)

    # Generate scatterplot
    generate_scatterplot(data, filenames, authors)
    

if __name__ == "__main__":
    main()