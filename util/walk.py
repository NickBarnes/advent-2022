import heapq

def walk(xmax, ymax, weight, start, diagonal=False):
    """Find the shortest path in a weighted grid (size `xmax` by `ymax`)
    from `start` to all other points, visiting orthogonal neighbours
    and diagonal neighbours if `diagonal`, skipping forbidden
    neighbours if `weight(node,neighbour)` is None.

    """

    def neighbours(x,y):
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (not diagonal) and dx and dy:
                    continue
                newx = x+dx
                newy = y+dy
                if newx >= 0 and newx < xmax and newy >= 0 and newy < ymax:
                    yield newx, newy

    grey = [(0, start)]
    far = {start: 0}

    while grey:
        d, pos = heapq.heappop(grey)
        r,c = pos
        if far[pos] < d: # already seen at shorter distance
            continue
        for n in neighbours(r, c):
            w = weight(pos, n)
            if w is not None and (n not in far or far[n] > d + w):
                heapq.heappush(grey, (d + w, n))
                far[n] = d + w
    return far
