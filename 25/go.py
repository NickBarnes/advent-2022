import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

def go(filename):
    print(f"results from {filename}:")
    lines = file.lines(filename)

    digits = '=-012'

    val = {}
    inv = {}
    for i,d in enumerate(digits):
        val[d] = i-2
        inv[i-2] = d

    def from_snafu(s):
        return val[s[-1]] + (from_snafu(s[:-1]) * 5 if len(s) > 1 else 0)

    def to_snafu(n):
        return inv[((n+2) % 5) - 2] + (to_snafu((n+2) // 5) if n > 2 else "")

    print(f"sum of fuel requirements (answer one) is {to_snafu(sum(from_snafu(l) for l in lines))}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
