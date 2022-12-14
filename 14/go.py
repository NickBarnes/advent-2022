import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

def go(filename):
    print(f"results from {filename}:")
    lines = file.lines(filename)
    points = [[(int(p[0]),int(p[1])) for item in line.split(' -> ') if (p := item.split(','))] for line in lines]
    pairs = [(l[i],l[i+1]) for l in points for i in range(len(l)-1)]
    points = [p for pair in pairs for p in pair]

    xmin = min(p[0] for p in points)
    xmax = max(p[0] for p in points)
    ymin = min(p[1] for p in points)
    ymax = max(p[1] for p in points)

    floor = ymax+2
    xmax = 500 + floor + 1
    xmin = 500 - floor - 1

    # Could offset by xmin at this point
    grid = [[' ' for x in range(xmax+1)] for y in range(floor+1)]

    # draw grid
    for (ax,ay),(bx,by) in pairs:
        if ax == bx:
            for y in range(min(ay,by),max(ay,by)+1):
                grid[y][ax] = '#'
        else: # ay == by
            for x in range(min(ax,bx),max(ax,bx)+1):
                grid[ay][x] = '#'

    for x in range(xmax+1):
        grid[floor][x] = '='

    # fill with sand
    sand = 0
    running = True
    overflow = False
    while running:
        sx,sy = 500,0
        while True:
            if sy >= ymax:
                if not overflow:
                    print(f"sand falls off bottom after {sand}")
                overflow = True
            if grid[sy+1][sx] == ' ':
                sy += 1
            elif grid[sy+1][sx-1] == ' ':
                sy += 1
                sx -= 1
            elif grid[sy+1][sx+1] == ' ':
                sy += 1
                sx += 1
            else:
                grid[sy][sx] = 'o'
                sand += 1
                if sy == 0 and sx == 500:
                    print(f"sand fills up infinite void after {sand}")
                    running = False
                break

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
