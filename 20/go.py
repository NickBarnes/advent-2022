import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

class Node:
    def __init__(self, v, k):
        self.val = v * k
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"<{self.val}>"

    def advance(self, m):
        if self.val == 0: # Don't move
            return

        x = self
        if self.val > 0:
            # end up after x
            for _ in range(self.val % m):
                x = x.next
        else:
            for _ in range((-self.val) % m):
                x = x.prev
            x = x.prev

        # unlink
        self.prev.next = self.next
        self.next.prev = self.prev
        # insert
        x.next.prev = self
        self.next = x.next
        self.prev = x
        x.next = self
        
def go(filename):
    print(f"results from {filename}:")

    def link(nodes):
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i+1]
            nodes[i+1].prev = nodes[i]
        nodes[0].prev = nodes[-1]
        nodes[-1].next = nodes[0]

    def mix(nodes):
        for n in nodes:
            n.advance(len(nodes)-1)

    def coords(nodes):
        n = next(n for n in nodes if n.val == 0)
        s = 0
        for _ in range(3):
            for i in range(1000):
                n = n.next
            s += n.val
        return s

    # part 1
    nodes = [Node(int(l), 1) for l in file.lines(filename)]
    link(nodes)
    mix(nodes)
    s = coords(nodes)
    print(f"sum of grove coordinates after mixing once without a key (answer one): {s}")

    # part 2
    key = 811589153
    nodes = [Node(int(l), key) for l in file.lines(filename)]
    link(nodes)

    for _ in range(10):
        mix(nodes)
    s = coords(nodes)
    print(f"sum of grove coordinates after mixing ten times with a key (answer two): {s}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
