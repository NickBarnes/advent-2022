import boiler
import heapq

def go(filename):
    print(f"results from {filename}:")
    chars = boiler.chars(filename)
    grid = [[0 if c == 'S' else 25 if c == 'E' else ord(c)-ord('a') for c in row] for row in chars]
    start = next((i, row.index('S')) for i, row in enumerate(chars) if 'S' in row)
    end = next((i, row.index('E')) for i, row in enumerate(chars) if 'E' in row)

    rows = len(grid)
    cols = len(grid[0])

    def neighbours(i,j):
        if i > 0: yield (i-1,j)
        if i < rows-1: yield (i+1,j)
        if j > 0: yield (i,j-1)
        if j < cols-1: yield (i,j+1)

    # reachability going down: may climb any amount but not descend more than 1
    def reach_neighbours(i,j,h):
        for ni,nj in neighbours(i,j):
            if h - grid[ni][nj] <= 1:
                yield ni,nj

    # set of points to look at, which we'll keep in closest-point-first order
    grey = [(0, end)]
    # shortest distance so far found to any given point
    far = {end: 0}

    while grey:
        d, pos = heapq.heappop(grey)
        r,c = pos
        if far[pos] <= d: # already seen at shorter distance
            continue
        d += 1
        for n in reach_neighbours(r,c, grid[r][c]):
            if n not in far or far[n] > d:
                heapq.heappush(grey, (d, n))
                far[n] = d

    print(f"shortest path from start to end is {far[start]}")

    shortest_climb = min(v for p,v in far.items() if grid[p[0]][p[1]] == 0)
    print(f"shortest path from low point to end is {shortest_climb}")

if __name__ == '__main__':
    for f in boiler.files():
        go(f)
