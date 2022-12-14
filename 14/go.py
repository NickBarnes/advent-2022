import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util'))

import walk
import file

# Visualisation. Just ignore everything with `if pil`.
try:
    from PIL import Image, ImageColor
    pil = True
except:
    pil = False

def go(filename):
    print(f"results from {filename}:")
    lines = file.lines(filename)
    points = [[(int(p[0]),int(p[1])) for item in line.split(' -> ') if (p := item.split(','))] for line in lines]
    pairs = [(l[i],l[i+1]) for l in points for i in range(len(l)-1)]
    points = [p for pair in pairs for p in pair]

    xmin = min(p[0] for p in points)
    xmax = max(p[0] for p in points)
    ymin = 0
    ymax = max(p[1] for p in points)

    floor = ymax+2
    xmax = 500 + floor + 1
    xmin = 500 - floor - 1

    # Could offset by xmin at this point
    grid = [[' ' for x in range(xmax+1)] for y in range(floor+1)]

    if pil:
        xsize = xmax - xmin + 1
        ysize = ymax - ymin + 1
        
        margin = 5
        frame_count = 0
    
        color = {' ': (255,255,255,255), # air
                 'o': (194,178,128,255), # first sand
                 'x': (240,220,170,255), # second sand
                 '#': (0,0,255,255),     # wall
                 '=': (255,0,0,255),     # floor
                 '?': (0,255,0,255),     # wut?
        }
        im = Image.new('RGB', (xsize + 2*margin, ysize + 2*margin), ImageColor.getrgb('white'))
        os.makedirs('frames', exist_ok=True)
        os.makedirs('snaps', exist_ok=True)

    def pix(x,y,c):
        grid[y][x] = c
        if pil:
            pix = color.get(c, color['?'])
            im.putpixel((x - xmin + margin, y - ymin + margin), pix)

    def frame(repeat=1):
        nonlocal frame_count
        if pil:
            for i in range(repeat):
                im.save(f"frames/{frame_count:05}.png")
                frame_count += 1

    def snapshot(name):
        if pil:
            scale = 1000 // im.size[0]
            im2 = im.resize((im.size[0]*scale, im.size[1]*scale), Image.Resampling.BOX)
            im2.save(f"snaps/{name}.png")

    frame(repeat=5)

    # draw grid
    for i, ((ax,ay),(bx,by)) in enumerate(pairs):
        if ax == bx:
            for y in range(min(ay,by),max(ay,by)+1):
                pix(ax,y,'#')
        else: # ay == by
            for x in range(min(ax,bx),max(ax,bx)+1):
                pix(x,ay,'#')
        if i % 10 == 0:
            frame()

    for x in range(xmin,xmax+1):
        pix(x, floor, '=')

    frame(repeat=10)
    snapshot('grid')

    # fill with sand
    sand = 0
    running = True
    overflow = False
    skip = 3 # how often do we want a frame before overflow?
    while running:
        sx,sy = 500,0
        while True:
            if sy >= ymax:
                if not overflow:
                    print(f"sand falls off bottom after {sand}")
                    overflow = True
                    snapshot('floor')
                    skip = 100 # how often do we want a frame now?
            if grid[sy+1][sx] == ' ':
                sy += 1
            elif grid[sy+1][sx-1] == ' ':
                sy += 1
                sx -= 1
            elif grid[sy+1][sx+1] == ' ':
                sy += 1
                sx += 1
            else:
                pix(sx,sy,'x' if overflow else 'o')
                if sand % skip == 0:
                    frame()
                sand += 1
                if sy == 0 and sx == 500:
                    print(f"sand fills up infinite void after {sand}")
                    running = False
                break

    frame(repeat=30)
    snapshot('end')

    # convert frames to a movie
    if pil:
        scale = 1000 // im.size[0]
        os.system(f"ffmpeg -r 30 -i frames/%05d.png -vf 'scale={im.size[0]*scale}:{im.size[1]*scale}' -c:v libx264 -profile:v baseline -tune animation -pix_fmt yuv420p {filename}.mp4")

if __name__ == '__main__':
    for f in file.files(__file__):
        go(f)
