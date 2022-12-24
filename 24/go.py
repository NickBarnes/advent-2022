import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

directions = {'>': (0,1),
             '<': (0,-1),
             '^': (-1,0),
             'v': (1,0),
}

def go(filename):
    print(f"results from {filename}:")
    map = file.chars(filename)
    rows = len(map)
    cols = len(map[0])
    assert all(len(r) == cols for r in map)
    
    blizzards = []   # (row, col, dr, dc)
    occupied = set() # locations of blizzards (row, col)
    walls = set()    # (row, col)

    for r in range(rows):
        for c in range(cols):
            if map[r][c] == '#':
                walls.add((r,c))
            elif map[r][c] in directions:
                blizzards.append((r,c,*directions[map[r][c]]))
                occupied.add((r,c))
    
    start = (0, next(i for i in range(cols) if map[0][i] == '.'))
    end = (rows-1, next(i for i in range(cols) if map[rows-1][i] == '.'))
    locations = {} # our possible locations

    def show():
        grid=[[' ' for _ in range(cols)] for _ in range(rows)]
        for r,c in walls:
            grid[r][c] = '#'
        for r,c in occupied:
            grid[r][c] = '*'
        for r,c in locations:
            grid[r][c] = '@'
        print('\n'.join(''.join(r) for r in grid))

    time = 0
    
    def find(start, goal):
        nonlocal time, blizzards, locations, occupied
        locations = {start: []}
        while True:
            # move blizzards
            whither = []
            occupied = set()
            for r,c,dr,dc in blizzards:
                while True:
                    r = (r+dr) % rows
                    c = (c+dc) % cols
                    if (r,c) not in walls:
                        break
                whither.append((r,c,dr,dc))
                occupied.add((r,c))
            blizzards = whither
            time += 1

            # move us
            whither = {}
            for (r,c),h in locations.items():
                for dr,dc in ((0,1),(0,-1),(-1,0),(1,0),(0,0)):
                    nr,nc = r+dr,c+dc
                    if (nr,nc) not in occupied and (nr,nc) not in walls and 0 <= nr < rows:
                        newh = h[:]
                        newh.append((nr,nc))
                        if (nr,nc) == goal:
                            # newh is the route. Could use for visualisation.
                            return newh
                        whither[(nr,nc)] = newh
            locations = whither

            if time % 100 == 0:
                print(f"time {time}")
                show()

    find(start, end)
    print(f"First arrive at end at time {time} (answer one):")
    show()

    find(end, start)
    print(f"First arrive back at start at time {time}:")
    show()

    find(start, end)
    print(f"Finally arrive back at the end at time {time} (answer two):")
    show()

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
