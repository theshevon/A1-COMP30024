"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: David Crowe, Shevon Mendis
"""

import sys
import json
from path_finder import PathFinder

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
    path_finder = PathFinder(data)
    path_finder.find_path()

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
