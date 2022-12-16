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
# (reversed route) do I follow to get it?

def best(pos, t, to_open):
    if t <= 0: # no time left
        return 0,[]
    score = pos.flow * (t-1)
    time_left = t-1 if pos.flow else t
    if to_open:
        next_best,route = max(best(v, time_left-pos.distances[v], to_open-{v}) for v in to_open)
    else:
        next_best,route = (0,[])
    route.append((pos, t))
    return (score + next_best, route)

# what's the best score we can produce if I arrive at `pos1` with time
# `t1` left, to open the valve there, and my pachyderm assistant
# arrives at `pos2` with time `t2` left, to open the valve there, with
# `to_open` *other* valves left to open. And what (reversed) routes do
# we each follow to get it?

def best2(pos1, t1, pos2, t2, to_open):
    if t1 > t2: # I arrive first to open my valve
        if 0 >= t1: # no time left
            return 0,[],[]
        score = pos1.flow * (t1-1)
        t1left = t1-1 if pos1.flow else t1
        if to_open: # more valves to open
            next_best, route1, route2 = max(best2(v, t1left-pos1.distances[v], pos2, t2, to_open-{v}) for v in to_open)
        else:
            next_best, route1, route2 = best2(None, 0, pos2, t2, set())
        route1.append((pos1, t1))
        return score + next_best, route1, route2
    elif t1 < t2: 
        next_best, route1, route2 = best2(pos2, t2, pos1, t1, to_open)
        return next_best, route2, route1
    else: # t1 == t2
        if 0 >= t1:
            return 0,[],[]
        if pos1 == pos2: # both at the same valve at the same time: only one of us opens it
            score = pos1.flow * (t1-1)
            t1left = t1-1 if pos1.flow else t1
            t2left = t2
        else: # we open two different valves in this minute
            score = (pos1.flow + pos2.flow) * (t1-1)
            t1left = t1-1 if pos1.flow else t1
            t2left = t2-1 if pos2.flow else t2
        if len(to_open) > 1:
            next_best, route1, route2 = max(max(best2(v1, t1left-pos1.distances[v1],
                                                      v2, t2left-pos2.distances[v2],
                                                      to_open-{v1} - {v2}) for v2 in to_open - {v1})
                                            for v1 in to_open)
        elif len(to_open) == 1: # race to the last valve
            v = to_open.pop()
            next_best, route1, route2 = best2(v, t1left-pos1.distances[v], None, 0, set())
            next_best_2, route1_2, route2_2 = best2(None, 0, v, t2left-pos2.distances[v], set())
            if next_best_2 > next_best:
                next_best, route1, route2 = next_best_2, route1_2, route2_2
        else: # no valves left
            next_best, route1, route2 = 0, [], []
        route1.append((pos1, t1))
        if pos1 != pos2:
            route2.append((pos2, t2))
        return score + next_best, route1, route2

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
    print('\n'.join(f"  I open {v.id} in minute {30-t}, scoring {(t-1)*v.flow}" for v,t in route[::-1] if v.flow))
    print(f"Total pressure released in 30 minutes (answer one): {score}")

    score, route1, route2 = best2(valves['AA'],26,valves['AA'],26,set(v for v in vs if v.flow))
    r = [(t,v,n) for r,n in [(route1, "I open"),(route2, "Tramples opens")] for v,t in r]
    r.sort()
    print('\n'.join(f" {n} valve {v.id} in minute {26-t}, scoring {(t-1)*v.flow}" for t,v,n in r if v.flow))
    print(f"total pressure released in 26 minutes with the help of Tramples the Crushera (answer two): {score}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
