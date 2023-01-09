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
# remaining time `t` and `to_open` other valves left to open, and what
# (reversed) route do I follow to get it?

cache = {}

def best(pos, t, to_open):
    key = (pos, t, frozenset(to_open))
    if key in cache:
        return cache[key]
    score = pos.flow * (t-1) # from opening this valve
    time_left = t-1 if pos.flow else t
    next_best,route = max((best(v, nt, to_open-{v})
                           for v in to_open
                           if (nt := time_left-pos.distances[v]) > 0),
                          default=(0,[]))
    route = route[:] + [(pos, t)]
    score += next_best
    cache[key] = (score, route)
    return score, route

# With the assistance of Tramples, Crusher of Enemies: maximise over
# all partitions of the valves into two sets (one for me, one for
# Tramples). Could doubtless do better than this but this is fairly
# quick.

import itertools

def best2(pos, t, closed):
    max, br1, br2 = 0, None, None
    for r in range(len(closed) // 2):
        for c in itertools.combinations(closed, r):
            h = frozenset(c)
            p1, r1 = best(pos, t, h)
            p2, r2 = best(pos, t, closed - h)
            if p1 + p2 > max:
                max, br1, br2 = p1 + p2, r1, r2
    return max, br1, br2

valve_re = re.compile("Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)")

def go(filename):
    print(f"results from {filename}:")
    lines = [valve_re.match(line).groups() for line in file.lines(filename)]
    vs = [Valve(v, int(f), vs.split(', ')) for v,f,vs in lines]
    for v in vs:
        v.resolve()

    for v in vs:
        v.dist()
    
    score, route = best(valves['AA'],30, set(v for v in vs if v.flow))
    print('\n'.join(f"  I open {v.id} in minute {30-t}, scoring {(t-1)*v.flow}"
                    for v,t in route[::-1] if v.flow))
    print(f"Total pressure released in 30 minutes (answer one): {score}")
    
    score, route1, route2 = best2(valves['AA'], 26, frozenset(v for v in vs if v.flow))
    r = [(t,v,n) for r,n in [(route1, "I open"),(route2, "Tramples opens")] for v,t in r]
    r.sort()
    print('\n'.join(f" {n} valve {v.id} in minute {26-t}, scoring {(t-1)*v.flow}"
                    for t,v,n in r if v.flow))
    print(f"total pressure released in 26 minutes with the help of Tramples, Crusher of Enemies (answer two): {score}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
