import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

def go(filename):
    print(f"results from {filename}:")
    chars = file.chars(filename)
    start = next((i, row.index('S')) for i, row in enumerate(chars) if 'S' in row)
    end = next((i, row.index('E')) for i, row in enumerate(chars) if 'E' in row)

    grid = {(i,j): 0 if c == 'S' else 25 if c == 'E' else ord(c)-ord('a')
            for i, row in enumerate(chars) for j,c in enumerate(row)}

    neighbours = walk.grid(len(chars), len(chars[0]))
    # reachability going down: may climb any amount but not descend more than 1
    def weights(a):
        for n in neighbours(a):
            if grid[a] - grid[n] <= 1: yield n,1

    shortest = walk.walk(end, weights)

    print(f"shortest path from start to end is {shortest[start]}")
    shortest_climb = min(v for p,v in shortest.items() if grid[p] == 0)
    print(f"shortest path from low point to end is {shortest_climb}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
