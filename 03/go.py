# items in rucksacks.

# each item is a letter with a value defined like this:
def val(c):
    if 'a' <= c <= 'z': return ord(c)-ord('a')+1
    return ord(c)-ord('A')+27

def go(filename):
    print(f"results from {filename}:")
    sacks = [l.strip() for l in open(filename,'r')]

    # Each sack has an even number of items, and one item in both
    # the first and second half. Total of the values of the duplicates:
    total = sum(val((set(s[:len(s)//2]) & set(s[len(s)//2:])).pop())
                for s in sacks)
    print(f"    odd items add to {total} (answer one)")

    # Each group of three sacks has one item in all three sacks (the
    # 'badge'). Total of the values of the badges.

    # There's some trick with zip() and iter() to get groups-of-N but
    # I can't remember it off-hand.
    badge_total = sum(val((set(group[0]) & set(group[1]) & set(group[2])).pop())
                      for group in [sacks[i:i+3]
                                    for i in range(0, len(sacks), 3)])
    print(f"    total badge priority {badge_total} (answer two)")

# Daily boilerplate for applying 'go' to files on the command-line or
# to input.txt if there are none.

import sys
import os

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
else:
    go(os.path.join(os.path.dirname(__file__), 'input.txt'))
