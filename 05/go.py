# Supply stacks

import re
move_re = re.compile('move ([0-9]+) from ([0-9]+) to ([0-9]+)')

def go(filename):
    print(f"results from {filename}:")
    stacks, moves = open(filename,'r').read().split('\n\n')

    # for each stack, go backwards through the stack lines getting the crate characters,
    # then strip to remove the spaces.
    crates = [list(''.join(stack).strip())
              for stack in zip(*stacks.split('\n')[::-1])
              if set(stack) - set('[] ')]

    # convert each move into n, a, b (for "move n from a to b")
    moves = list([int(g) for g in move_re.match(l).groups()]
                 for l in moves.split('\n') if l)

    # copy the crate stacks so we can manipulate them twice
    crates_1 = [stack[:] for stack in crates]

    # part 1: move one crate at at time
    for n,a,b in moves:
        for i in range(n):
            crates_1[b-1].append(crates_1[a-1].pop())
    top_crates = ''.join(crate[-1] for crate in crates_1)
    print(f"    answer one (one crate at a time): {top_crates}")

    # part 2: move n crates at at time
    for n,a,b in moves:
        crates[b-1] += crates[a-1][-n:]
        crates[a-1] = crates[a-1][:-n]
    top_crates = ''.join(crate[-1] for crate in crates)
    print(f"    answer two (N crates at a time): {top_crates}")

# daily boilerplate for applying 'go' to files on the command-line or
# to input.txt if there are none.

import sys
import os

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
else:
    go(os.path.join(os.path.dirname(__file__), 'input.txt'))
