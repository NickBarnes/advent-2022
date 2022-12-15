# Day 15

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file
import re
line_re = re.compile('Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)')


def go(filename):
    print(f"results from {filename}:")
    lines = file.lines(filename)
    input = (map(int,line_re.match(line).groups()) for line in lines)

    def dist(x1,y1,x2,y2): return abs(x1-x2)+abs(y1-y2)
    def sign(x): return -1 if x < 0 else 1 if x > 0 else 0

    signals = [(sx,sy,bx,by,dist(sx,sy,bx,by)) for sx,sy,bx,by in input]

    # find blocks of ruled-out cells, and beacons, on a given line
    def testline(y):
        # Cost proportional to #signals
        blocked = []
        beacons = set()
        for sx,sy,bx,by,d in signals:
            if by == y:
                beacons.add(bx)
            dx = d - abs(sy-y)
            if dx < 0:
                continue
            blocked.append([sx-dx,sx+dx])
        blocked.sort()
        # eliminate overlaps
        i = 0
        while i < len(blocked)-1:
            while i < len(blocked)-1 and blocked[i][1] >= blocked[i+1][0]-1:
                blocked[i][1] = max(blocked[i][1], blocked[i+1][1])
                del blocked[i+1]
            i = i + 1
        return blocked, beacons

    # part 1:
    testy = 10 if 'test' in filename else 2000000
    blocked, beacons = testline(testy)
    blocked_cells = sum(b[1]-b[0]+1 for b in blocked) - len(beacons)
    print(f"Blocked cells on line {testy} (answer one): {blocked_cells}")

    # part 2
    xmax, ymax = (20,20) if 'test' in filename else (4000000, 4000000)

    def part2_1():
        # Attempt 1.
        # Look at each line, find an unblocked cell.
        # Cost proportional to search dimension * signals. Runtime 36s.
        for y in range(ymax):
            blocked, _ = testline(y)
            if blocked[0][0] > 0:
                return 0, y
            for i in range(len(blocked)):
                if blocked[i][0] > xmax:
                    break
                if blocked[i][1] < xmax:
                    return blocked[i][1]+1, y

    def part2_2():
        # Attempt 2: can we go faster?
        # Go around just outside the perimeter of each diamond.
        # Cost proportional to signals*signals*(typical range). Runtime 43 seconds.
        for sx,sy,bx,by,d in signals:
            for x in range(sx-d-1,sx+d+2):
                if x < 0 or x > xmax:
                    continue
                dx=abs(sx-x)
                dy=d+1-dx
                for y in (sy-dy,sy+dy):
                    if y < 0 or y > ymax:
                        continue
                    # can this x,y be seen?
                    seen = False
                    for s2x,s2y,_,_,d2 in signals:
                        if dist(x,y,s2x,s2y) <= d2:
                            seen = True
                            break
                    if not seen:
                        return x,y

    def part2_3():
        # Third attempt. This is more like it. Runtime 0.03 seconds.
        # Find pairs of signals which agree on an edge. The cell we're looking for
        # must be on two such lines, intersecting.
        inc = set() # values C for edges y - x = C
        dec = set() # values D for edges y + x = D
        for i, (x1,y1,_,_,d1) in enumerate(signals):
            for x2,y2,_,_,d2 in signals[i+1:]:
                if dist(x1,y1,x2,y2) == d1 + d2 + 2:
                    if sign(x1-x2) == sign(y1-y2):
                        # decreasing edge, x + y = D
                        xy1 = x1+y1
                        xy2 = x2+y2
                        dec.add(xy1 + sign(xy2-xy1)*(d1+1))
                    else:
                        # increasing edge, y - x = C
                        yx1 = y1-x1
                        yx2 = y2-x2
                        inc.add(yx1 + sign(yx2-yx1)*(d1+1))

        # for all intersections, if not ruled out by another signal
        # then it is good.
        for C in inc:
            for D in dec:
                # x + y = D, y - x = C, so 2y= C + D, 2x = D-C
                x, y = (D-C)/2, (C+D)/2
                if x != int(x): # half-integral solutions no good
                    continue
                good = True
                for sx,sy,_,_,d in signals:
                    if dist(sx,sy,x,y) <= d:
                        good = False
                        break
                if good:
                    return int(x),int(y)

    x,y = part2_3()
    print(f"answer two (distress beacon at {x},{y}): {x*4000000 + y}")
    # x,y = part2_1()
    # print(f"answer two (distress beacon at {x},{y}): {x*4000000 + y}")
    # x,y = part2_2()
    # print(f"answer two (distress beacon at {x},{y}): {x*4000000 + y}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
