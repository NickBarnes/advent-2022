# Heads and tails

directions = {'U': (0, 1),
              'D': (0, -1),
              'L': (-1, 0),
              'R': (1, 0),
}

def sign(a):
    return 1 if a > 0 else -1 if a < 0 else 0

def follow(lines, len):
    rope = [[0,0] for _ in range(len)]
    visited = set()
    for l,line in enumerate(lines):
        dx,dy = directions[line[0]]
        for i in range(int(line[1])):
            rope[0][0] += dx
            rope[0][1] += dy
            for k in range(1,len):
                h = rope[k-1]
                t = rope[k]
                if abs(h[0]-t[0]) > 1 or abs(h[1]-t[1]) > 1: # tail moves
                    t[0] += sign(h[0]-t[0])
                    t[1] += sign(h[1]-t[1])
            visited.add((rope[-1][0],rope[-1][1]))
    return visited

def go(filename):
    print(f"results from {filename}:")
    lines = [l.strip().split() for l in open(filename,'r')]
    short_visits = follow(lines, 2)
    print(f"Unique locations visited by a short rope's tail (answer one): {len(short_visits)}")
    long_visits = follow(lines, 10)
    print(f"Unique locations visited by a long rope's tail (answer one): {len(long_visits)}")

# daily boilerplate for applying 'go' to files on the command-line or
# to input.txt if there are none.

import sys
import os

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
else:
    go(os.path.join(os.path.dirname(__file__), 'input.txt'))
