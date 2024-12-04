# boilerplate function for reading a file in different ways. Returns:
# - a list of lists of the lines in each section (separated by blank lines)
# - a list of the lines in the file
# - a list of lists of words on each line
# - a list of lists of digits on every line of a digit-grid file

def read(filename):
    # sometimes we want sections, sometimes we want lines
    sections = [[l.strip() for l in s.strip().split('\n')] for s in open(filename,'r').read().split('\n\n')]
                
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
    _, _, words, _ = read(filename)
    cycle = 0
    x = 1
    # total signal strength
    signal = 0
    # pixel grid
    grid = [['?' for _ in range(40)] for _ in range(6)]

    def tick():
        nonlocal cycle, signal, grid
        row = cycle // 40
        col = cycle % 40
        cycle += 1 # this is now the true cycle number (AoC counters start from 1)
        if col == 19: # offset by one (AoC counters start from 1)
            signal += x * cycle
        grid[row][col]= '#' if abs(x-col) < 2 else ' '

    for line in words:
        if line[0] == "noop":
            tick()
        elif line[0] == 'addx':
            tick()
            tick()
            x += int(line[1])

    print(f"total signal strength (answer one): {signal}")
    print("answer two is these letters:")
    print('\n'.join(''.join(row) for row in grid))

# daily boilerplate for applying 'go' to files on the command-line.

import sys

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
