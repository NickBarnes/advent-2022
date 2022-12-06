# Comms handset

# Find first position with N unique consecutive characters.

def go(filename):
    print(f"results from {filename}:")
    for l in open(filename,'r'):
        if not l.strip(): continue
        print(f"message {l[:10]}...({len(l)}):")
        print("  answer one (4 unique)",
              next(i for i in range(4, len(l)) if len(set(l[i-4:i])) == 4))
        print("  answer two (14 unique)",
              next(i for i in range(14, len(l)) if len(set(l[i-14:i])) == 14))

# daily boilerplate for applying 'go' to files on the command-line or
# to input.txt if there are none.

import sys
import os

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
else:
    go(os.path.join(os.path.dirname(__file__), 'input.txt'))
