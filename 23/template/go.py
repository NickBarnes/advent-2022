import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

def go(filename):
    print(f"results from {filename}:")
    # pick one:
    # sections = file.sections(filename)
    # lines = file.lines(filename)
    # words = file.words(filename)
    # digits = file.digits(filename)
    # chars = file.chars(filename)

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
