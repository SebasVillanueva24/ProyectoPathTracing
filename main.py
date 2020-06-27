import numpy as np
import pygame
import random
from PIL import Image
from Point import *
from Segment import *
import rt
import math
import threading

def iluminacionIndirecta():
    #Funcion recursiva
    #Tirar rayos desde la fuente a todas las direcciones
    #Calcular intensidad que pega con el segmento y convertirlo en una fuente de luz la cual va a tirar rayos en todas las direcciones desde ese pto, varias veces
    #Puede imitar ilum directa

def iluminacionDirecta():
    while True:
        point = Point(random.uniform(0,500), random.uniform(0,500))

        pixel = 0

        for source in sources:
            dir = source - point

            length = rt.length(dir)

            free = True
            for seg in segments:
                dist = rt.raySegmentIntersect(point, rt.normalize(dir), seg.a, seg.b)
                if dist != -1 and dist < length:
                    free = False
                    break

            if free:
                intensity = (1 - (length / 500)) ** 2
                # print(len)
                # intensity = max(0, min(intensity, 255))
                values = (ref[int(point.y)][int(point.x)])[:3]
                # combine color, light source and light color
                values = values * intensity * light

                # add all light sources
                pixel += values

            # average pixel value and assign
            px[int(point.x)][int(point.y)] = pixel // len(sources)



def raytrace():
    # Raytraces the scene progessively
    while True:
        # random point in the image
        point = Point(random.uniform(0, 500), random.uniform(0, 500))
        # pixel color
        pixel = 0

        for source in sources:
            # calculates direction to light source

            dir = source - point
            # add jitter
            # dir.x += random.uniform(0, 25)
            # dir.y += random.uniform(0, 25)

            # distance between point and light source
            length = rt.length(dir)
            # normalized distance to source
            #length2 = rt.length(rt.normalize(dir))
            '''
            for seg in segments:
                            # check if ray intersects with segment
                            dist = rt.raySegmentIntersect(point, dir, seg.a, seg.b)
                            # if intersection, or if intersection is closer than light source
                            if dist > 0 and length2 > dist:
                                free = False
                                break
            '''
            free = True
            for seg in segments:
                dist = rt.raySegmentIntersect(point, rt.normalize(dir), seg.a, seg.b)
                if dist != -1 and dist < length:
                    free = False
                    break


            if free:
                intensity = (1 - (length / 500)) ** 2
                # print(len)
                # intensity = max(0, min(intensity, 255))
                values = (ref[int(point.y)][int(point.x)])[:3]
                # combine color, light source and light color
                values = values * intensity * light

                # add all light sources
                pixel += values

            # average pixel value and assign
            px[int(point.x)][int(point.y)] = pixel // len(sources)

def getFrame():
    # grabs the current image and returns it
    pixels = np.roll(px, (1, 2), (0, 1))
    return pixels


# pygame stuff
h, w = 550, 550
border = 50
pygame.init()
screen = pygame.display.set_mode((w + (2 * border), h + (2 * border)))
pygame.display.set_caption("2D Path tracing")
done = False
clock = pygame.time.Clock()

# init random
random.seed()

# image setup
i = Image.new("RGB", (500, 500), (0, 0, 0))
px = np.array(i)

# reference image for background color
im_file = Image.open("fondo2.png")
ref = np.array(im_file)
#Point(30, 200), Point(310, 300)
# light positions
sources = [Point(415, 125)]
'''sources = []
for i in range(80, 100):
    sources.append(Point(i+50, 200))'''
# light color
light = np.array([1, 1, 1])
# light = np.array([1, 1, 1])

# warning, point order affects intersection test!!
#Rombo, cuadrado, triangulo
segments = [
    #bordes
    #(Segment(Point(25, 25), Point(425, 25))),
    #(Segment(Point(425, 25), Point(425, 425))),
    #(Segment(Point(425, 425), Point(25, 425))),
    #(Segment(Point(25, 425), Point(25, 25))),

    (Segment(Point(100, 250), Point(200, 250))),
    (Segment(Point(100, 250), Point(150, 350))),
    (Segment(Point(150, 350), Point(250, 350))),
    (Segment(Point(200, 250), Point(250, 350))),

    #(Segment(Point(390, 100), Point(440, 100))),
    (Segment(Point(440, 100), Point(440, 150))),
    (Segment(Point(440, 150), Point(390, 150))),
    (Segment(Point(390, 150), Point(390, 100)))
]

'''segments = [
    ([Point(180, 135), Point(215, 135)]),
    ([Point(285, 135), Point(320, 135)]),
    ([Point(320, 135), Point(320, 280)]),
    ([Point(320, 320), Point(320, 355)]),
    ([Point(320, 355), Point(215, 355)]),
    ([Point(180, 390), Point(180, 286)]),
    ([Point(180, 286), Point(140, 286)]),
    ([Point(320, 320), Point(360, 320)]),
    ([Point(180, 250), Point(180, 135)]),
]'''

# thread setup
t = threading.Thread(target=pathtrace)  # f being the function that tells how the ball should move
t.setDaemon(True)  # Alternatively, you can use "t.daemon = True"
t.start()

# main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear screen to white before drawing
    screen.fill((255, 255, 255))

    # Get a numpy array to display from the simulation
    npimage = getFrame()

    # Convert to a surface and splat onto screen offset by border width and height
    surface = pygame.surfarray.make_surface(npimage)
    screen.blit(surface, (border, border))

    pygame.display.flip()
    clock.tick(60)
