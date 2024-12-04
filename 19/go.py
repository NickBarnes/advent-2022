import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

materials = 'ore clay obsidian geode'.split()
GEODE=3

robot_re = re.compile('.*Each ([a-z]+) robot costs (.*)')

class Blueprint:
    def __init__(self,ls):
        self.id = int(ls[0].split(':')[0])
        self.recipes = []
        for l in ls:
            if (m := robot_re.match(l)):
                mat = materials.index(m.group(1))
                res = m.group(2).split(' and ')
                recipe = [0,0,0,0]
                for r in res:
                    recipe[materials.index(r.split(' ')[1])] += int(r.split(' ')[0])
                self.recipes.append((mat, recipe))
        self.max_robots = [max(r[m] for _,r in self.recipes) for m in range(4)]
        self.cache = {}
        self.hits = 0

    # return the maximum number of geodes we might have at the end,
    # given `resources` and `robots` when we have `time` total time
    # remaining.
    def geodes_(self, time, resources, robots):
        if time <= 0:
            # out of time!
            return resources[GEODE]
        # memoized
        key = (time, tuple(resources), tuple(robots))
        if key in self.cache:
            self.hits += 1 # for stats
            return self.cache[key]

        # baseline is do nothing to the end of time
        m = resources[GEODE] + robots[GEODE] * time

        if time > 1: # might be worth making a robot
            for material, recipe in self.recipes:
                if material < GEODE and robots[material] >= self.max_robots[material]:
                    # already have as many robots of this kind as we can use
                    continue
                # work out how long we would have to wait to make this robot
                wait = 0
                can_make = True
                for i,req in enumerate(recipe):
                    if not req:
                        continue
                    if not robots[i]: # can't do this recipe
                        can_make = False
                        break
                    wait = max(wait, (req - resources[i] + robots[i] - 1) // robots[i])
                if can_make and time > wait + 1: # let's try making this robot
                    new_time = time - wait - 1
                    new_resources = list(resources)
                    for i in range(4):
                        new_resources[i] += robots[i] * (wait + 1) # fresh production
                        new_resources[i] -= recipe[i]              # cost of robot
                        # try to improve cache hit by throwing away excess resources
                        # (any more than we could possibly use in the time remaining)
                        # this made my solution about ten times faster by improving cache hit rate,
                        # but test.txt is still hopelessly slow (actual puzzle input is OK).
                        if i < 3:
                            new_resources[i] = min(new_resources[i], self.max_robots[i] * new_time)
                    new_robots = robots[:]
                    new_robots[material] += 1
                    # how well can we do after we've made it?
                    m = max(m, self.geodes_(new_time, new_resources, new_robots))

        self.cache[key] = m
        return m

    def geodes(self, time):
        geodes = self.geodes_(time, [0,0,0,0], [1,0,0,0])
        print(f"Blueprint {self.id} gets {geodes} in {time} with cache size {len(self.cache)} and {self.hits} hits")
        return geodes

    def quality(self, time):
        geodes = self.geodes(time)
        return self.id * geodes

def go(filename):
    print(f"results from {filename}:")
    blueprints = [Blueprint(bp.strip().split('.')) for bp in open(filename,'r').read().split('Blueprint ') if bp.strip()]
    answer_one = sum(b.quality(24) for b in blueprints)
    print(f"total quality in 24 minutes with all blueprints: {answer_one}")
    answer_two = 1
    for b in blueprints:
        if b.id < 4:
            answer_two *= b.geodes(32)
    print(f"product of geodes counts in 32 minutes from first three blueprints: {answer_two}")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
