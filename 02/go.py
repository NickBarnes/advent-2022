import sys
import os
import re
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

response_A = {'X': R,
              'Y': P,
              'Z': S,
}

response_B = {'X': L,
              'Y': D,
              'Z': W,
}

strat_re = re.compile('([ABC]) ([XYZ])')

def go(filename):
    print(f"results from {filename}:")
    written = [strat_re.match(l.strip()).groups() for l in open(filename,'r')]
    strategy_A = [(opponent[g[0]],response_A[g[1]]) for g in written]
    scores_A = [result_score[result[(r,o)]]+shape_score[r] for (o,r) in strategy_A]
    print(f"total score A (answer one) {sum(scores_A)}")
    strategy_B = [(o,r) for g in written if (o := opponent[g[0]]) if (res := response_B[g[1]]) if (r := choose[(o, res)])]
    scores_B = [result_score[result[(r,o)]]+shape_score[r] for (o,r) in strategy_B]
    print(f"total score B (answer two) {sum(scores_B)}")

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
else:
    go(os.path.join(os.path.dirname(__file__), 'input.txt'))
