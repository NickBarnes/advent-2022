import heapq

def walk(start, weights):
    """Find the shortest paths in a weighted network from `start` to all
    other nodes.

    """
    grey = [(0, start)]
    shortest = {start: 0}

    while grey:
        d, p = heapq.heappop(grey)
        if shortest[p] < d: # already seen at shorter distance
            continue
        for n,w in weights(p):
            if n not in shortest or shortest[n] > d + w:
                heapq.heappush(grey, (d + w, n))
                shortest[n] = d + w
    return shortest

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
