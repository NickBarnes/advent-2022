import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file
import functools

# This works but feels like cheating. Also I'm really not keen on
# calling eval on unvalidated input. I guess I could match it against
# '[\[\],0-9]+' first, as no string matching that could give my
# computer to a hacker.
#
# def make_list(s):
#     return eval(s)
#
# So after getting the right answer, I wrote this:

def make_list_inner(s, i=0):
    """returns list, next index to read."""
    l = []
    i += 1 # skipping the '['
    while True:
        if s[i] == ',':
            i += 1
        elif s[i] == ']':
            return l, i+1 # skipping the ']'
        elif s[i] == '[':
            sub,i = make_list_inner(s,i)
            l.append(sub)
        else: # parse an int
            n = 0
            while s[i].isdigit():
                n = n * 10 + int(s[i])
                i += 1
            l.append(n)

def make_list(s):
    return make_list_inner(s)[0]

# Traditional comparison function: -1 if a < b, 0 if a == b, 1 if a > b

def compare(a,b):
    if isinstance(a, int):
        if isinstance(b, int):
            return -1 if b > a else 0 if b == a else 1
        else: # b is a list so make a into a list
            a = [a]
    if not isinstance(b, list):
        b = [b]
    # a and b both lists
    if not a: # empty list
        if b:
            return -1
        else:
            return 0
    if not b:
        return 1
    # recurse down both lists
    return compare(a[0],b[0]) or compare(a[1:],b[1:])

def go(filename):
    print(f"results from {filename}:")
    sections = [(make_list(s[0]), make_list(s[1])) for s in file.sections(filename)]

    right_order_count = sum(i for i,s in enumerate(sections,start=1) if compare(s[0],s[1]) == -1)

    packets = [p for s in sections for p in s] + [[2]] + [[6]]
    packets.sort(key=functools.cmp_to_key(compare))
    d1 = next(i for i,p in enumerate(packets, start=1) if compare(p,[[2]]) == 0)
    d2 = next(i for i,p in enumerate(packets, start=1) if compare(p,[[6]]) == 0)

    print(f"product of indexes of pairs in right order (answer one): {right_order_count}")
    print(f"decoder key (answer two): {d1*d2}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
