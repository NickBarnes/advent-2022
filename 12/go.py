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

    # reachability going down: may climb any amount but not descend more than 1
    def weight(a,b):
        return 1 if grid[a] - grid[b] <= 1 else None

    far = walk.walk(weight, end, walk.grid(len(chars), len(chars[0])))

    print(f"shortest path from start to end is {far[start]}")
    shortest_climb = min(v for p,v in far.items() if grid[p] == 0)
    print(f"shortest path from low point to end is {shortest_climb}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
