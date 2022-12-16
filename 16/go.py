import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file
import re

valves = {}

class Valve:
    def __init__(self,id,flow,tunnels):
        self.id = id
        self.flow = flow
        self.tunnels = tunnels
        valves[self.id] = self

    def resolve(self):
        self.neighbours = set(valves[t] for t in self.tunnels)

    def dist(self):
        self.distances = walk.walk(self, lambda v: ((t,1) for t in v.neighbours))

    def __lt__(self,other):
        return self.id < other.id

    def __repr__(self):
        return f"<{self.id}:{self.flow}>"

# what's the best score if I arrive at valve `pos` to open it, with
# remaining time `t` and `to_open` valves left to open, and what
# (reversed route) do I follow to get it?

def best(pos, t, to_open):
    if t <= 0: # no time left
        return 0,[]
    score = pos.flow * (t-1)
    time_left = t-1 if pos.flow else t
    left = to_open-{pos}
    if left:
        next_best,route = max(best(v, time_left-pos.distances[v], left) for v in left)
    else:
        next_best,route = (0,[])
    route.append((pos, t))
    return (score + next_best, route)

# what's the best score we can produce if I arrive at `pos1` with time
# `t1` left, to open the valve there, and my pachyderm assistant
# arrives at `pos2` with time `t2` left, to open the valve there, with
# `to_open` *other* valves left to open. What (reversed) routes do
# we follow to get it?

def best2(pos1, t1, pos2, t2, to_open):
    if t1 > t2: # I arrive first and open my valve
        if 0 >= t1: # no time left
            return 0,[],[]
        score = pos1.flow * (t1-1)
        t1left = t1-1 if pos1.flow else t1
        left = to_open-{pos1}
        next_best,route1, route2 = 0, [], []
        if left: # more valves to open
            next_best,route1,route2 = max(best2(v, t1left-pos1.distances[v], pos2, t2, left-{v}) for v in left)
        route1.append((pos1, t1))
        return (score + next_best, route1, route2)
    elif t1 < t2: 
        next_best, route1, route2 = best2(pos2, t2, pos1, t1, to_open)
        return next_best, route2, route1
    else: # t1 == t2
        if 0 >= t1:
            return 0,[],[]
        if pos1 == pos2: # only one of us opens the valve
            score = pos1.flow * (t1-1)
            t1left = t1-1 if pos1.flow else t1
            t2left = t2
        else: # we open two different valves in this minute
            score = (pos1.flow + pos2.flow) * (t1-1)
            t1left = t1-1 if pos1.flow else t1
            t2left = t2-1 if pos2.flow else t2
        left = to_open-{pos1,pos2}
        if len(left) > 1:
            next_best, route1, route2 = 0,[],[]
            for v1 in left: # my next valve
                trial, r1, r2 = max(best2(v1, t1left-pos1.distances[v1], v2, t2left-pos2.distances[v2], left-{v1} - {v2}) for v2 in left - {v1})
                if trial > next_best:
                    next_best, route1, route2 = trial, r1, r2
        elif len(left) == 1: # race to the last valve
            v = left.pop()
            next_best, route1, route2 = best2(v, t1left-pos1.distances[v], None, 0, set())
            b, r12, r22 = best2(None, 0, v, t1left-pos2.distances[v], set())
            if b > next_best:
                next_best, route1, route2 = b, r12, r22
        else: # no valves left
            next_best, route1, route2 = 0, [], []
        route1.append((pos1, t1))
        if pos1 != pos2:
            route2.append((pos2, t2))
        return (score + next_best, route1, route2)

valve_re = re.compile("Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)")
def go(filename):
    print(f"results from {filename}:")
    lines = [valve_re.match(line).groups() for line in file.lines(filename)]
    vs = [Valve(v, int(f), vs.split(', ')) for v,f,vs in lines]
    for v in vs:
        v.resolve()

    for v in vs:
        v.dist()
    
    print(best(valves['AA'],30, set(v for v in vs if v.flow)))
    print(best2(valves['AA'],26,valves['AA'],26,set(v for v in vs if v.flow)))

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
