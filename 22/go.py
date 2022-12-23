import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

import re
dir_re = re.compile('([0-9]*)([LR])')

compass = [(1,0),(0,1),(-1,0),(0,-1)]

# Wrapping map for a plain toroidal wrapping from edge to edge without
# changing direction.

def rect_wrap(map):
    width = max(len(m) for m in map)
    height = len(map)
    for i in range(height):
        map[i] = map[i] + ' '*(width-len(map[i]))

    wrap = {}
    for x in range(width):
        ymin = next(y for y,l in enumerate(map) if l[x] != ' ')
        ymax = next(y for y,l in reversed(list(enumerate(map))) if l[x] != ' ')
        wrap[(x,ymin,3)] = (x,ymax,3)
        wrap[(x,ymax,1)] = (x,ymin,1)
    for y in range(height):
        xmin = next(x for x in range(width) if map[y][x] != ' ')
        xmax = next(x for x in range(width-1,-1,-1) if map[y][x] != ' ')
        wrap[(xmin,y,2)] = (xmax,y,2)
        wrap[(xmax,y,0)] = (xmin,y,0)
    return wrap

# Wrapping map for a cube net like this:

#    A
#  BCD
#    EF

def small_cube_wrap(map, edge):
    wrap = {}
    for i in range(edge):
        # top edge of A, top edge of B
        wrap[(2*edge  +i, 0*edge    , 3)] = (1*edge-1-i, 1*edge    , 1)
        wrap[(1*edge-1-i, 1*edge    , 3)] = (2*edge  +i, 0*edge    , 1) 
        # left edge of A, top edge of C
        wrap[(2*edge    , 0*edge  +i, 2)] = (1*edge  +i, 1*edge    , 1)
        wrap[(1*edge  +i, 1*edge    , 3)] = (2*edge    , 0*edge  +i, 0)
        # right edge of A, right edge of F
        wrap[(3*edge-1  ,         +i, 0)] = (4*edge-1  , 3*edge-1-i, 2)
        wrap[(4*edge-1  , 3*edge-1-i, 0)] = (3*edge-1  ,         +i, 2)
        # left edge of B, bottom edge of F
        wrap[(0*edge    , 1*edge  +i, 2)] = (4*edge-1-i, 3*edge-1  , 3)
        wrap[(4*edge-1-i, 3*edge-1  , 1)] = (0*edge    , 1*edge  +i, 0)
        # bottom edge of B, bottom edge of E
        wrap[(0*edge  +i, 2*edge-1  , 1)] = (3*edge-1-i, 3*edge-1  , 3)
        wrap[(3*edge-1-i, 3*edge-1  , 1)] = (0*edge  +i, 2*edge-1  , 3)
        # bottom edge of C, left edge of E
        wrap[(1*edge  +i, 2*edge-1  , 1)] = (2*edge    , 3*edge-1-i, 0)
        wrap[(2*edge    , 3*edge-1-i, 2)] = (1*edge  +i, 2*edge-1  , 3)
        # right edge of D, top edge of F
        wrap[(3*edge-1  , 1*edge  +i, 0)] = (4*edge-1-i, 2*edge    , 1)
        wrap[(4*edge-1-i, 2*edge    , 3)] = (3*edge-1  , 1*edge  +i, 2)
    return wrap

# Is a wrapping map valid? Could do more checks here.

def check_wrap(map, wrap):
    for a in wrap:
        b = wrap[a]
        b_=(b[0],b[1],(b[2]+2) % 4)
        assert b_ in wrap
        c = wrap[b_]
        assert a[:2] == c[:2]
        assert a[2] == (c[2]+ 2) % 4
        assert map[a[1]][a[0]] != ' '
        assert map[b[1]][b[0]] != ' '

# Wrapping map for a cube net like this:

#  AB
#  C
# DE
# F

def large_cube_wrap(map, edge):
    wrap = {}
    for i in range(edge):
        # left edge of C, top edge of D
        wrap[(1*edge    , 1*edge  +i, 2)] = (0*edge  +i, 2*edge    , 1)
        wrap[(0*edge  +i, 2*edge    , 3)] = (1*edge    , 1*edge  +i, 0) 
        # bottom edge of B, right edge of C
        wrap[(2*edge  +i, 1*edge-1  , 1)] = (2*edge-1  , 1*edge  +i, 2)
        wrap[(2*edge-1  , 1*edge  +i, 0)] = (2*edge  +i, 1*edge-1  , 3)
        # left edge of A, left edge of D (upside-down)
        wrap[(1*edge    , 0*edge  +i, 2)] = (0*edge    , 3*edge-1-i, 0)
        wrap[(0*edge    , 3*edge-1-i, 2)] = (1*edge    , 0*edge  +i, 0)
        # top edge of A, left edge of F
        wrap[(1*edge  +i, 0*edge    , 3)] = (0*edge    , 3*edge  +i, 0)
        wrap[(0*edge    , 3*edge  +i, 2)] = (1*edge  +i, 0*edge    , 1)
        # top edge of B, bottom edge of F
        wrap[(2*edge  +i, 0*edge    , 3)] = (0*edge  +i, 4*edge-1  , 3)
        wrap[(0*edge  +i, 4*edge-1  , 1)] = (2*edge  +i, 0*edge    , 1)
        # right edge of F, bottom edge of E
        wrap[(1*edge-1  , 3*edge  +i, 0)] = (1*edge  +i, 3*edge-1  , 3)
        wrap[(1*edge  +i, 3*edge-1  , 1)] = (1*edge-1  , 3*edge  +i, 2)
        # right edge of B, right edge of E (upside-down)
        wrap[(3*edge-1  , 0*edge  +i, 0)] = (2*edge-1  , 3*edge-1-i, 2)
        wrap[(2*edge-1  , 3*edge-1-i, 0)] = (3*edge-1  , 0*edge  +i, 2)
    return wrap

# Wander around the map according to the directions

def trace(map, wrap, directions):
    facing = 0
    y = 0
    x = next(i for i in range(len(map[y])) if map[y][i] == '.')
    for dist,turn in directions:
        dx,dy = compass[facing]
        for _ in range(dist):
            if (x,y,facing) in wrap:
                nx,ny,nf = wrap[(x,y,facing)]
            else:
                ny,nx,nf = y+dy,x+dx,facing
            if map[ny][nx] == '#': # stop
                break
            facing = nf
            dx, dy = compass[facing]
            if map[ny][nx] != '.':
                print(len(map), len(map[ny]), ny, nx)
            assert map[ny][nx] == '.'
            y,x = ny,nx
        facing = (facing + turn) % len(compass)
    return y,x,facing

def go(filename):
    print(f"results from {filename}:")
    lines = list(open(filename,'r'))
    dirs = lines[-1]
    map = [l[:-1] for l in lines[:-2]]
    directions = []
    while m := dir_re.match(dirs):
        dirs = dirs[m.end():]
        directions.append((int(m.group(1)), -1 if m.group(2) == 'L' else 1))
    directions.append((int(dirs),0))

    wrap = rect_wrap(map)
    y,x,facing = trace(map, wrap, directions)
    rect_grove = 1000 * (y+1) + 4 * (x+1) + facing
    print(f"Grove location on rectangular map (answer one): {rect_grove}")
    
    nonblank = sum(1 for l in map for c in l if c != ' ')
    assert nonblank % 6 == 0
    single_face = nonblank // 6
    edge = single_face ** 0.5
    assert edge == int(edge)
    edge = int(edge)

    if edge == 4: # test data
        wrap = small_cube_wrap(map, edge)
    else: # puzzle data
        wrap = large_cube_wrap(map, edge)

    check_wrap(map, wrap)
    y,x,facing = trace(map, wrap, directions)
    cube_grove = 1000 * (y+1) + 4 * (x+1) + facing
    print(f"Grove location on cuboidal map (answer two): {cube_grove}")


if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
