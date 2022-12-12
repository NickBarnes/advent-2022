import heapq

def walk(weight, start, neighbours):
    """Find the shortest path in a weighted network from `start` to all
    other nodes, visiting all neighbours, skipping forbidden
    neighbours if `weight(node,neighbour)` is None.

    """
    grey = [(0, start)]
    far = {start: 0}

    while grey:
        d, pos = heapq.heappop(grey)
        if far[pos] < d: # already seen at shorter distance
            continue
        for n in neighbours(pos):
            w = weight(pos, n)
            if w is not None and (n not in far or far[n] > d + w):
                heapq.heappush(grey, (d + w, n))
                far[n] = d + w
    return far

def grid(xmax, ymax, diagonal=False):
    """Return a neighbour function for a 2D grid size `xmax` by `ymax`. If
    `diagonal` then include diagonal neighbours.

    """
    def neighbours(p):
        x,y = p
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (not diagonal) and dx and dy:
                    continue
                newx = x+dx
                newy = y+dy
                if newx >= 0 and newx < xmax and newy >= 0 and newy < ymax:
                    yield newx, newy
    return neighbours
