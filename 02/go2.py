# R=0, P=1, S=2
# W=1, L=2, D=0

# if we play 'a' and the opponent plays b, what's the outcome?
def outcome(a,b): return (a-b) % 3

# if the opponent plays `a` and we want outcome `o`, what should we play?
def choose(a,o): return (o+a) % 3
def shape_score(s): return s+1
def result_score(r): return (r * 3 + 3) % 9

# in both parts 1 and 2, A/B/C indicates R/P/S of the opponent
def opponent(c): return 'ABC'.index(c)

# in part 1, we think that X/Y/Z indicates R/P/S
def response_A(c): return 'XYZ'.index(c)

# in part 2, we discover that X/Y/Z actually indicates L/D/W
def response_B(c): return ('XYZ'.index(c) - 1) % 3

def round_score(play, other):
    return result_score(outcome(play, other)) + shape_score(play)

def go(filename):
    print(f"results from {filename}:")
    written = [l.strip().split() for l in open(filename,'r')]

    strategy_A = [(opponent(o), response_A(r)) for o,r in written]
    scores_A = [round_score(r,o) for (o,r) in strategy_A]
    print(f"total score A (answer one) {sum(scores_A)}")

    strategy_B = [(o := opponent(a), choose(o,response_B(b))) for a,b in written]
    scores_B = [round_score(r,o) for (o,r) in strategy_B]
    print(f"total score B (answer two) {sum(scores_B)}")

# Daily boilerplate for applying 'go' to files on the command-line or
# to input.txt if there are none.

import sys
import os

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
else:
    go(os.path.join(os.path.dirname(__file__), 'input.txt'))
