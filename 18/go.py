import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

def go(filename):
    print(f"results from {filename}:")
    lines = file.lines(filename)
    cubes=set(tuple(map(int,l.split(','))) for l in lines)
    d = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

    def surface():
        return sum((x+dx,y+dy,z+dz) not in cubes for x,y,z in cubes for dx,dy,dz in d)

    # cells from which steam can escape to the outside
    escaping = set()
    # cells from which it cannot
    trapped = set()

    xmin = min(x for x,y,z in cubes)
    xmax = max(x for x,y,z in cubes)
    ymin = min(y for x,y,z in cubes)
    ymax = max(y for x,y,z in cubes)
    zmin = min(z for x,y,z in cubes)
    zmax = max(z for x,y,z in cubes)

    # can steam in this cell escape to the outside?
    def escape(x,y,z):
        nonlocal escaping, trapped
        if (x,y,z) in trapped:
            return False
        grey = set()
        grey.add((x,y,z))
        black = set()
        while grey:
            gx,gy,gz = grey.pop()
            for dx,dy,dz in d:
                nx, ny, nz = gx + dx, gy + dy, gz + dz
                if (nx,ny,nz) in cubes or (nx,ny,nz) in black:
                    continue
                if ((nx,ny,nz) in escaping or not
                    (xmin < nx < xmax and ymin < ny < ymax and zmin < nz < zmax)):
                    # reached an escaping cell, so every cell we've looked at escapes
                    escaping = escaping | grey | black
                    return True
                grey.add((nx,ny,nz))
            black.add((gx,gy,gz))
        trapped = trapped | black
        return False

    # fill in any cells which can't escape to the outside
    def fill():
        for x in range(xmin+1,xmax):
            for y in range(ymin+1,ymax):
                for z in range(zmin+1,zmax):
                    if not (x,y,z) in cubes and not escape(x,y,z):
                        cubes.add((x,y,z))

    print(f"answer one (surface area): {surface()}")

    # Now fill in all trapped cells
    fill()
    print(f"  Found {len(escaping)} escaping cells and {len(trapped)} trapped cells")
    print(f"answer two (exposed surface area): {surface()}")


if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
