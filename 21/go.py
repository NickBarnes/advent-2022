# Day 21. This could have been horrible, including a general
# polynomial solver. But AoC wouldn't do that to us, so what is it?
# Could have been quadratic, but turns out just to be a straight
# linear equation. Boring!

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

monkeys = {}

class Monkey:
    def __init__(self,s):
        self.name, val = s.split(':')
        self.order_ = None
        self.coeffs_ = None
        vparts = val.split()
        if len(vparts) == 1:
            self.given = True
            self.value_ = int(vparts[0])
        else:
            self.given = False
            self.value_ = None
            self.left = vparts[0]
            self.op = vparts[1]
            self.right = vparts[2]
        monkeys[self.name] = self
    
    def resolve(self):
        if not self.given:
            self.left = monkeys[self.left]
            self.right = monkeys[self.right]

    def clear(self):
        if not self.given:
            self.value_ = None

    def value(self):
        if self.value_ is None:
            left = self.left.value()
            right = self.right.value()
            if self.op == '+':
                self.value_ = left + right
            elif self.op == '-':
                self.value_ = left - right
            elif self.op == '*':
                self.value_ = left * right
            elif self.op == '/':
                self.value_= left / right
        return self.value_

    def order(self):
        "What order of polynomial do I have here?"
        if self.order_ is None:
            if self.given:
                self.order_ = 1 if self.name == 'humn' else 0
            else:
                left = self.left.order()
                right = self.right.order()
                if self.op in '+-':
                    self.order_ = max(left, right)
                elif self.op == '*':
                    if left > 0 and right > 0:
                        print("mul", left, right)
                    self.order_ = left + right
                elif self.op == '/':
                    if right > 0:
                        print("div", left, right)
                    self.order_ = left - right
        return self.order_

    # triple: constant, coefficient, denominator
    def coeffs(self):
        if self.coeffs_ is None:
            if self.given:
                return (0,1,1) if self.name == 'humn' else (self.value_, 0,1)
            else:
                left = self.left.coeffs()
                right = self.right.coeffs()
                if self.op == '+':
                    self.coeffs_ = (left[0]*right[2]+right[0]*left[2],left[1]*right[2]+right[1]*left[2],left[2]*right[2])
                elif self.op == '-':
                    self.coeffs_ = (left[0]*right[2]-right[0]*left[2],left[1]*right[2]-right[1]*left[2],left[2]*right[2])
                elif self.op == '*':
                    assert left[1] == 0 or right[1] == 0
                    self.coeffs_ = (left[0]*right[0], left[0]*right[1] + left[1]*right[0], left[2]*right[2])
                elif self.op == '/':
                    assert right[1] == 0
                    self.coeffs_ = (left[0]*right[2],left[1]*right[2],left[2] * right[0])
        return self.coeffs_

def go(filename):
    print(f"results from {filename}:")
    for l in file.lines(filename):
        Monkey(l)
    for m in monkeys.values():
        m.resolve()
    print(f"Answer one, taking 'humn' value as {monkeys['humn'].value()}: {monkeys['root'].value()}")

    # (ax+b)/c = (dx+e)/f

    b,a,c = monkeys['root'].left.coeffs()
    e,d,f = monkeys['root'].right.coeffs()

    # multiply through by cf: afx + bf = dcx + ec
    A = a * f
    B = b * f
    D = d * c
    E = e * c

    # bring terms to the left

    A -= D
    B -= E

    # sanity check

    assert B % A == 0
    
    print(f"Answer two, what 'humn' value for root to balance: {-B/A}")
    
if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
