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

def generate_scatterplot(data, filenames, authors):
    """
    Generate a scatterplot of commits per week and per author.
    """
    x=filenames
    y=random.sample(range(0, 50), len(filenames))
    # Create the colors list using the function above
    authors_colored=assign_color(authors)
    print(authors_colored)

    plt.scatter(x=x,y=y,s=500) #Pass on the list created by the function here
    plt.grid(True)
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