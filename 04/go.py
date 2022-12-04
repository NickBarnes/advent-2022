# Elf cleaning ranges

# Does the first range wholly contain the second?
def contain(r1,r2):
    return r2[0] >= r1[0] and r2[1] <= r1[1]

# Do the two ranges overlap at all?
def overlap(r1,r2):
    return r1[0] <= r2[1] and r2[0] <= r1[1]

def go(filename):
    print(f"results from {filename}:")
    ranges = [l.strip().split(',') for l in open(filename,'r')]
    values = [[(int(s[0]),int(s[1])) for r in l if (s := r.split('-'))] for l in ranges]

    c1 = sum(1 for v in values if contain(*v) or contain(*reversed(v)))
    print(f"pairs wholly overlap (answer one) {c1}")

    c2 = sum(1 for v in values if overlap(*v))
    print(f"pairs partly overlap (answer two) {c2}")

# daily boilerplate for applying 'go' to files on the command-line or
# to input.txt if there are none.

import sys
import os

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
else:
    go(os.path.join(os.path.dirname(__file__), 'input.txt'))
