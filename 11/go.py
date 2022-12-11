import boiler
import re

# Monkey 1:
#   Starting items: 54, 65, 75, 74
#   Operation: new = old + 6
#   Test: divisible by 19
#     If true: throw to monkey 2
#     If false: throw to monkey 0

id_re = re.compile('Monkey ([0-9]+):')
start_re = re.compile('Starting items: ([0-9, ]+)')
operation_re = re.compile('Operation: new = (.+)')
test_re = re.compile('Test: divisible by ([0-9]+)')
true_re = re.compile('If true: throw to monkey ([0-9]+)')
false_re = re.compile('If false: throw to monkey ([0-9]+)')

relieving = True

monkeys = {}

# all arithmetic can happen modulo this number (because that's all any
# of the monkeys care about).
bigmod = None

class Monkey:
    def __init__(self, spec):
        self.spec = spec
        self.id = int(id_re.match(spec[0]).group(1))
        monkeys[self.id] = self
        starts = start_re.match(spec[1]).group(1).split(', ')
        self.items = [int(item) for item in starts]
        left, self.op, right = operation_re.match(spec[2]).group(1).split()
        self.left = None if left == 'old' else int(left)
        self.right = None if right == 'old' else int(right)
        assert self.op in '+*'
        self.divisor = int(test_re.match(spec[3]).group(1))
        self.if_true = int(true_re.match(spec[4]).group(1))
        self.if_false = int(false_re.match(spec[5]).group(1))
        self.inspections = 0

    def go(self):
        for item in self.items:
            self.inspections += 1
            # perform operation on item, including division
            left = item if self.left is None else self.left
            right = item if self.right is None else self.right
            newitem = (left + right) if self.op == '+' else (left * right)
            if relieving:
                newitem = newitem // 3 # relief
            newitem = newitem % bigmod
            test = (newitem % self.divisor) == 0
            monkeys[self.if_true if test else self.if_false].receive(newitem)
            self.items = []

    def receive(self, item):
        self.items.append(item)

def read(filename):
    global monkeys, bigmod
    monkeys = {}
    bigmod = 1
    for s in boiler.sections(filename):
        bigmod *= Monkey(s).divisor

def action(filename, rounds, relief):
    global monkeys, relieving
    read(filename)
    relieving = relief
    for r in range(rounds):
        for k in range(len(monkeys)):
            monkeys[k].go()

def business(k, tag):
    final = sorted(monkeys.values(), key=lambda m: m.inspections)
    business = final[-1].inspections * final[-2].inspections
    print(f"monkey business {tag} (answer {k}) {business}")

def go(filename):
    print(f"results from {filename}:")
    action(filename, 20, True)
    business("one", "after 20 rounds with relief")

    action(filename, 10000, False)
    business("two", "after 10,000 rounds with no relief")

if __name__ == '__main__':
    for f in boiler.files():
        go(f)
