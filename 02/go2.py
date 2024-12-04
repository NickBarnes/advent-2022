# Rock, Paper, Scissors. We play `a`, opponent plays `b`, outcome is
# `o`.

# If we say R=0, P=1, S=2, W=1, L=2, D=0, then we have this handy
# modular arithmetic: o = a-b (mod 3)


# if we play `a` and the opponent plays `b`, what's the outcome `o`?
def outcome(a,b): return (a-b) % 3

# if the opponent plays `b` and we want outcome `o`, what should we play?
def choose(b,o): return (o+b) % 3

# Weird scoring rules
def shape_score(a): return a+1
def outcome_score(a, b): return (outcome(a,b) * 3 + 3) % 9

def score(a, b):
    return outcome_score(a, b) + shape_score(a)

# in both parts 1 and 2, A/B/C indicates R/P/S of the opponent
def opponent(c): return 'ABC'.index(c)

# in part 1, we think that X/Y/Z indicates R/P/S
def xyz_play(c): return 'XYZ'.index(c)

# in part 2, we discover that X/Y/Z actually indicates L/D/W
def xyz_outcome(c): return ('XYZ'.index(c) - 1) % 3

def go(filename):
    print(f"results from {filename}:")
    written = [l.strip().split() for l in open(filename,'r')]

    # each game is b,a for consistency with part 2 (where that's easier)
    games_1 = ((opponent(x), xyz_play(y)) for x,y in written)
    score_1 = sum(score(a,b) for b,a in games_1)
    print(f"total score 1 (answer one) {score_1}")

    # each game is b,a (because that's easier in this walrusy comprehension)
    games_2 = ((b := opponent(x), choose(b, xyz_outcome(y))) for x,y in written)
    score_2 = sum(score(a,b) for b,a in games_2)
    print(f"total score 2 (answer two) {score_2}")

# Daily boilerplate for applying 'go' to files on the command-line.

import sys

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
