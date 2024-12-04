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
    crates_copy = [stack[:] for stack in crates]

    # move N crates from stack a to stack b
    def move(a,b,n):
        crates[b-1] += crates[a-1][-n:]
        crates[a-1] = crates[a-1][:-n]
    
    # report the set of top crates
    def done(desc):
        top_crates = ''.join(crate[-1] for crate in crates)
        print(f"    {desc}: {top_crates}")

    # part 1: move one crate at at time
    for n,a,b in moves:
        for i in range(n):
            move(a,b,1)
    done("one crate at a time")

    crates = crates_copy
    # part 2: move n crates at at time
    for n,a,b in moves:
        move(a,b,n)
    done("N crates at a time")

# daily boilerplate for applying 'go' to files on the command-line.

import sys

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
