import sys
import os
from enum import Enum

# rock paper scissors. Wow, this was horrible.

Play = Enum('Play', ['Rock', 'Paper', 'Scissors'])
Outcome = Enum('Outcome', ['Win', 'Draw', 'Lose'])
R = Play.Rock
P = Play.Paper
S = Play.Scissors
W = Outcome.Win
D = Outcome.Draw
L = Outcome.Lose

# What's the outcome of a game?
result = {(R,R): D,
          (R,P): L,
          (R,S): W,
          (P,R): W,
          (P,P): D,
          (P,S): L,
          (S,R): L,
          (S,P): W,
          (S,S): D,
}

# Given an opponent's play, and a desired outcome, what play should I make?
choose = {(R,W): P,
          (R,D): R,
          (R,L): S,
          (P,W): S,
          (P,D): P,
          (P,L): R,
          (S,W): R,
          (S,D): S,
          (S,L): P,
}

# Each shape has a score, because of course it does.
shape_score = {R: 1,
               P: 2,
               S: 3,
}

result_score = {L: 0,
                D: 3,
                W: 6,
}

opponent = {'A': R,
            'B': P,
            'C': S
}

# in part 1, we think that X/Y/Z indicates R/P/S
response_A = {'X': R,
              'Y': P,
              'Z': S,
}

# in part 2, we discover that X/Y/Z actually indicates L/D/W
response_B = {'X': L,
              'Y': D,
              'Z': W,
}

def round_score(play, other):
    return result_score[result[(play, other)]] + shape_score[play]

def go(filename):
    print(f"results from {filename}:")
    written = [l.strip().split() for l in open(filename,'r')]

    strategy_A = [(opponent[o], response_A[r]) for o,r in written]
    scores_A = [round_score(r,o) for (o,r) in strategy_A]
    print(f"total score A (answer one) {sum(scores_A)}")

    strategy_B = [(o,choose[(o,res)]) for a,b in written
                  if (o := opponent[a])
                  if (res := response_B[b])]
    scores_B = [round_score(r,o) for (o,r) in strategy_B]
    print(f"total score B (answer two) {sum(scores_B)}")

# Daily boilerplate for applying 'go' to files on the command-line or
# to input.txt if there are none.

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
else:
    go(os.path.join(os.path.dirname(__file__), 'input.txt'))
