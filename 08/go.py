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

# How many trees can (i,j) see in direction (di,dj)? This is a bit
# grody (but much nicer than my first attempt).

def see(trees,i,j,di,dj):
    # are these coordinates in the forest?
    def inbounds(p):
        return p[0] >= 0 and p[0] < len(trees) and p[1] >= 0 and p[1] < len(trees[p[0]])
    # does this tree block the view?
    def blocking(p):
        return trees[p[0]][p[1]] >= trees[i][j]
    # all the possible locations for trees in this direction, to infinity!
    view = ((i+di*n,j+dj*n) for n in itertools.count(1))
    # trees we can see in that direction
    visible = takeuntil(itertools.takewhile(inbounds, view), blocking)
    return len(list(visible))

def score(trees, i, j):
    return see(trees,i,j,1,0) * see(trees,i,j,-1,0) * see(trees,i,j,0,1) * see(trees,i,j,0,-1)

def go(filename):
    print(f"results from {filename}:")
    trees = [[int(c) for c in l.strip()] for l in open(filename,'r')]
    visible_trees = sum(1 for i in range(len(trees)) for j in range(len(trees[i])) if visible(trees, i, j))
    print(f"Number of visible trees (answer one): {visible_trees}")
    max_score = max(score(trees,i,j) for i in range(len(trees)) for j in range(len(trees[i])))
    print(f"Highest scenery score (answer two): {max_score}")

# daily boilerplate for applying 'go' to files on the command-line.

import sys

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
