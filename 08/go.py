# Trees in the forest

# Can a tree be seen from outside the forest?

def visible(trees, i,j):
    return (all(trees[i][j] > trees[i][k] for k in range(j+1, len(trees[i]))) or
            all(trees[i][j] > trees[i][k] for k in range(j)) or
            all(trees[i][j] > trees[k][j] for k in range(i+1, len(trees))) or
            all(trees[i][j] > trees[k][j] for k in range(i)))

import itertools

# this should be in itertools
def takeuntil(iter, c):
    for v in iter:
        yield v
        if c(v):
            break

# are these coordinates in the forest?
def inbounds(trees, i, j):
    return i >= 0 and i < len(trees) and j >= 0 and j < len(trees[i])

# How many trees can (i,j) see in direction (di,dj)? This is a bit
# grody (but much nicer than my first attempt).

def see(trees,i,j,di,dj):
    view = ((i+di*n,j+dj*n) for n in itertools.count(1)) # indefinite view in that direction
    all = itertools.takewhile(lambda p: inbounds(trees,p[0],p[1]), view) # within the forest
    visible = takeuntil(all, lambda x: trees[x[0]][x[1]] >= trees[i][j])
    return len(list(visible))

def score(trees, i, j):
    return see(trees,i,j,1,0) * see(trees,i,j,-1,0) * see(trees,i,j,0,1) * see(trees,i,j,0,-1)

def go(filename):
    print(f"results from {filename}:")
    trees = [[int(c) for c in l.strip()] for l in open(filename,'r')]
    print(sum(1 for i in range(len(trees)) for j in range(len(trees[i])) if visible(trees, i, j)))
    print(max(score(trees,i,j) for i in range(len(trees)) for j in range(len(trees[i]))))

# daily boilerplate for applying 'go' to files on the command-line or
# to input.txt if there are none.

import sys
import os

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
else:
    go(os.path.join(os.path.dirname(__file__), 'input.txt'))
