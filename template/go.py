# boilerplate for reading a file in different ways. Returns:
# - a list of lists of the lines in each section (separated by blank lines)
# - a list of the lines in the file
# - a list of lists of words on each line
# - a list of lists of digits on every line of a digit-grid file

def read(filename):
    # sometimes we want sections, sometimes we want lines
    sections = [[l.strip() for l in s.strip().split('\n') for s in open(filename,'r').read().split('\n\n')]
    lines = [l.strip() for l in open(filename,'r')]

    # often if we want lines we also want parts of each line
    words = [l.split() for l in lines]

    # sometimes each line is just some digits making a grid
    try:
        grid = [int(c) for l in lines for c in l]
    except:
        grid = [[]]
    return sections, lines, words, grid
    

def go(filename):
    print(f"results from {filename}:")
    sections, lines, words, grid = read(filename)

# daily boilerplate for applying 'go' to files on the command-line or
# to input.txt if there are none.

import sys
import os

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
else:
    go(os.path.join(os.path.dirname(__file__), 'input.txt'))
