import sys
import os

def go(filename):
    print(f"results from {filename}:")
    elves = [e.split() for e in open(filename, 'r').read().split('\n\n')]
    calories = sorted([sum(int(l) for l in e) for e in elves])
    print(f"  answer 1 (max calories of any elf): {calories[-1]}")
    print(f"  answer 2 (total calories of top three elves): {sum(calories[-3:])}")

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        go(arg)
else:
    go(os.path.join(os.path.dirname(__file__), 'input.txt'))
