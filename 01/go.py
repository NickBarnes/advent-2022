import sys

input='input.txt'
if len(sys.argv) > 1:
    input = sys.argv[1]

elves = open(input,'r').read().split('\n\n')
calories = [sum(int(l) for l in e.split()) for e in elves]
print(f"answer 1 (max calories of any elf): {max(calories)}")
calories.sort()
print(f"answer 2 (total calories of top three elves): {sum(calories[-3:])}")
