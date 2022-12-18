import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

rock_defs = [
    ['####',
    ],[
        '.#.',
        '###',
        '.#.',
    ],['..#',
       '..#',
       '###',
    ],['#',
       '#',
       '#',
       '#',
    ],['##',
       '##',
    ]]

# Shifted rocks. rocks[i] is the ith rock in each of its possible positions from the left edge.

# Each shifted rock is a list of rows, counting from the bottom row of
# the rock. Each row is a number, the bit pattern of which is the
# cells occupied by that row of the rock. We also need the rock in the
# two impossible positions (one too far left and one too far right),
# to collision test against the left and right hand walls.

def get_rocks():
    return [[[sum(1<<(i+j+1) if c == '#' else 0 for i,c in enumerate(l)) for l in r[::-1]] for j in range(8)] for r in rock_defs]

def go(filename):
    print(f"results from {filename}:")
    rocks = get_rocks()
    jets = [-1 if c == '<' else 1 for c in open(filename,'r').read().strip()]

    # experimentally observed maximum roof depth of 28.
    KEYLENGTH=40

    def drop(count):
        # tower
        g = [511]  # floor
        # height of top-most rock
        top = 0
        jet_index = 0
        # maximum interesting roof depth
        roof = 0
        # hash table, rock index, jet index, pattern -> drop number, height
        memory = {}
        # height skipped during cycles
        height_skipped = 0
        # drop number
        drop = 0
        
        def test(r,h): # can shifted rock 'r' go at height 'h'?
            return all(r[i] & g[h+i] == 0 for i in range(len(r)))
        
        while drop < count:
            rock_index = drop % len(rocks)
            key = (rock_index, jet_index, tuple(g[top-KEYLENGTH:top]))
            if key in memory:
                drops_before_cycle, height_before_cycle = memory[key]
                cycle_length = drop - drops_before_cycle
                height_per_cycle = top - height_before_cycle
                cycles = (count - drop) // cycle_length
                drops_skipped = cycles * cycle_length
                height_skipped = cycles * height_per_cycle
                print(f"  After {drop} drops, at height {top}, we have matched a length-{KEYLENGTH} top pattern again:")
                print(f"    rock {rock_index}, jet {jet_index}, last seen at drop {drops_before_cycle}, height {height_before_cycle}.")
                print(f"  So we will now skip {drops_skipped} drops ({cycles} cycles), adding {height_skipped} height.")
                drop += drops_skipped
                # clear memory so we don't see all the other repeats
                memory = {}
            memory[key] = drop, top
                
            r = rocks[rock_index]
            h = len(r[0]) # height of rock
            b = top+4 # bottom line of the rock
            x = 2 # "Each rock appears so that its left edge is two units away from the left wall"
            for _ in range(len(g),b+h):
                g.append(257) # walls

            while test(r[x], b):
                newx = x + jets[jet_index]
                if test(r[newx], b):
                    x = newx
                b -= 1
                jet_index = (jet_index + 1) % len(jets)
                    
            # Last drop failed so rock ends up at b+1
            for i in range(h):
                g[b+1+i] |= r[x][i]
            if roof < top - b+1:
                roof = top-b+1
            top = max(top, b+h)
            drop += 1
        print(f"  maximum pertinent roof height found {roof}")
        print(f"  maximum actual height of grid {top}")
        return top + height_skipped

    top = drop(2022)
    print(f"answer one (height after 2022 drops): {top}")
    top = drop(1_000_000_000_000)
    print(f"answer two (height after a trillion drops): {top}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
