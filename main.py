import numpy as np
import pygame
import random
from PIL import Image
from Point import *
from Segment import *
import rt
import math
import threading

def reboteEspecular(sources,lights,ver,hemis,dir):
    dir.x = dir.x * -1

    point = sources

    sigo = True

    point.x = point.x + dir.x
    point.y = point.y + dir.y

    print(point)
        #if ((point.x > 0 and point.x < 500) and (point.y > 0 and point.y < 500)):
            #sigo = False

    pixel = 0

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
        values = values * intensity * lights

        # add all light sources
        pixel += values

    # average pixel value and assign
    # print(str(point.x)+" ++ "+str(point.y))
    px[int(point.x)][int(point.y)] = pixel


def rebote(sources,lights,tipo,ver,hemis,originalLight):

    if tipo == "difuso":
        cantPtos = random.randint(25, 50)
        if ver == False:

            for c in range(cantPtos):

                # mirar la posicion de la luz

                if hemis:
                    point = Point(random.uniform(1, 500), random.uniform(1, sources.y - 1))
                else:
                    point = Point(random.uniform(1, 500), random.uniform(sources.y + 1, 500))

                pixel = 0

                dir = sources - point
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
                    values = values * intensity * lights

                    # add all light sources
                    pixel += values

                # average pixel value and assign
                #print(str(point.x)+" ++ "+str(point.y))
                px[int(point.x)][int(point.y)] = pixel

        else:
            for c in range(cantPtos):

                # mirar la posicion de la luz

                if hemis:
                    point = Point(random.uniform(sources.x+1, 500), random.uniform(1, 500))
                else:
                    point = Point(random.uniform(1, sources.x-1), random.uniform(1, 500))

                pixel = 0

                dir = sources - point
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
                    values = values * intensity * lights

                    # add all light sources
                    pixel += values

                # average pixel value and assign
                #print(str(point.x)+" ++ "+str(point.y))
                px[int(point.x)][int(point.y)] = pixel
    elif tipo == "especular":
        if ver:
            return
        else:
            if hemis:
                v1 = originalLight - sources
                diff = sources.y - originalLight.y

                normal = Point(sources.x, diff)
                v2 = normal - sources

                cos = [rt.cosAngle(originalLight, normal, sources)]
                angle = np.arccos(cos)

                v3 = Point(math.cos(angle), math.sin(angle))
                aPintar = v3 + sources





def iluminacionIndirecta():

    for segmento in segments:

        if(segmento.vertical):

            free = True

            for p in range(segmento.a.y, segmento.b.y):

                point = Point(segmento.a.x, p)

                pixel = 0  # px[int(point.x)][int(point.y)]

                for i in range(0, len(sources)):
                    source = sources[i]

                    dir = source - point
                    print(dir)

                    length = rt.length(dir)

                    for seg in segments:

                        dist = rt.raySegmentIntersect(point, rt.normalize(dir), seg.a, seg.b)

                        if dist != -1 and dist < length:
                            if rt.intersectionPoint(point, rt.normalize(dir),
                                                    dist).x != point.x and rt.intersectionPoint(
                                    point, rt.normalize(dir), dist).y != point.y:
                                if seg.tipo != "transparente":
                                    free = False
                                break

                    if free:
                        for seg in segments:
                            dist = rt.raySegmentIntersect(point, rt.normalize(dir), seg.a, seg.b)

                            if dist != -1 and dist < length:
                                if rt.intersectionPoint(point, rt.normalize(dir),dist).x != point.x and rt.intersectionPoint(point, rt.normalize(dir), dist).y != point.y:
                                    break
                                else:

                                    intensity = (1 - (length / 500)) ** 2
                                    # print(len)
                                    # intensity = max(0, min(intensity, 255))
                                    values = (ref[int(point.y)][int(point.x)])[:3]
                                    # combine color, light source and light color
                                    values = values * intensity * lights[i]

                                    # add all light sources
                                    pixel += values

                                    pixel = pixel // len(sources)

                                    # px[int(point.x)][int(point.y)] = pixel // len(sources)

                                    pSources = Point(int(point.x), int(point.y))

                                    # light color
                                    pLights = [np.array([1, 1, 1])]

                                    if (source.x > int(point.x)):
                                        if segmento.tipo == "especular":
                                           reboteEspecular(pSources,pLights,False,True,dir)
                                        else:
                                            rebote(pSources, pLights, segmento.tipo, True, True,source)
                                    else:
                                        if segmento.tipo == "especular":
                                            reboteEspecular(pSources, pLights, False, False, dir)
                                        else:
                                            rebote(pSources, pLights, segmento.tipo, True, False, source)

                    if not free:
                        break
                if not free:
                    break


        else:

            free = True

            for p in range(segmento.a.x,segmento.b.x):

                point = Point(p, segmento.a.y)

                pixel = 0  # px[int(point.x)][int(point.y)]

                for i in range(0, len(sources)):
                    source = sources[i]

                    dir = source - point

                    length = rt.length(dir)

                    for seg in segments:

                        dist = rt.raySegmentIntersect(point, rt.normalize(dir), seg.a, seg.b)

                        if dist != -1 and dist < length:
                            if rt.intersectionPoint(point, rt.normalize(dir), dist).x != point.x and rt.intersectionPoint(
                                    point, rt.normalize(dir), dist).y != point.y:
                                if seg.tipo != "transparente":
                                    free = False
                                break


                    if free:
                        for seg in segments:
                            dist = rt.raySegmentIntersect(point, rt.normalize(dir), seg.a, seg.b)

                            if dist != -1 and dist < length:
                                if rt.intersectionPoint(point, rt.normalize(dir), dist).x != point.x and rt.intersectionPoint(
                                        point, rt.normalize(dir), dist).y != point.y:
                                    break
                                else:

                                    intensity = (1 - (length / 500)) ** 2
                                    # print(len)
                                    # intensity = max(0, min(intensity, 255))
                                    values = (ref[int(point.y)][int(point.x)])[:3]
                                    # combine color, light source and light color
                                    values = values * intensity * lights[i]

                                    # add all light sources
                                    pixel += values

                                    pixel = pixel // len(sources)

                                    # px[int(point.x)][int(point.y)] = pixel // len(sources)

                                    pSources = Point(int(point.x), int(point.y))

                                    # light color
                                    pLights = [np.array([1, 1, 1])]


                                    if(source.y<int(point.y)):
                                        if segmento.tipo == "especular":
                                            reboteEspecular(pSources, pLights, False, True, dir)
                                        else:
                                            rebote(pSources, pLights, segmento.tipo, True, True, source)
                                    else:
                                        if segmento.tipo == "especular":
                                            reboteEspecular(pSources, pLights, False, False, dir)
                                        else:
                                            rebote(pSources, pLights, segmento.tipo, True, False, source)
                    if not free:
                        break
                if not free:
                    break

def iluminacionDirecta():  # voy a hacer cambios
    while True:
        point = Point(random.uniform(0,500), random.uniform(0,500))

        if (px[int(point.x)][int(point.y)][:3] == 0).all():
            #negro
            pixel = 0
            negro = True

        else:
            #color
            pixel = px[int(point.x)][int(point.y)][:3]
            negro = False


        #for source in sources:
        for i in range(0,len(sources)):
            source = sources[i]

            dir = source - point

            length = rt.length(dir)

            free = True
            for seg in segments:
                dist = rt.raySegmentIntersect(point, rt.normalize(dir), seg.a, seg.b)
                if dist != -1 and dist < length:
                    if seg.tipo != "transparente":
                        free = False
                    break

            if free:
                intensity = (1 - (length / 500)) ** 2
                # print(len)
                # intensity = max(0, min(intensity, 255))
                values = (ref[int(point.y)][int(point.x)])[:3]
                # combine color, light source and light color
                values = values * intensity * lights[i]

                #print(values)
                # add all light sources

                if negro:
                    pixel += values
                else:
                    pixel = pixel + values

            # average pixel value and assign
            px[int(point.x)][int(point.y)] = pixel // len(sources)


def iluminacionTotal():
    iluminacionIndirecta()
    iluminacionDirecta()

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
im_file = Image.open("fondo3.png")
ref = np.array(im_file)

# light positions
sources = [Point(415, 125),Point(30, 200), Point(310, 410)]

# light color
lights = [np.array([0.65, 0.086, 0.79]),np.array([1, 1, 1]),np.array([0.18, 0.94, 0.80])] # cambiar color
# light = np.array([1, 1, 1])

# warning, point order affects intersection test!!
#Rombo, cuadrado, triangulo
segments = [
    (Segment(Point(100, 250), Point(200, 250), "especular", False)),
    (Segment(Point(200, 250), Point(200, 350), "difuso", True)),
    (Segment(Point(200, 350), Point(100, 350), "difuso", False )),
    (Segment(Point(100, 350), Point(100, 250), "difuso", True)),

    #cuadrado morado
    (Segment(Point(390, 100), Point(440, 100), "difuso", False )),
    (Segment(Point(440, 100), Point(440, 150), "difuso", True )),
    (Segment(Point(390, 150), Point(440, 150), "difuso", False)),# abajo
    (Segment(Point(390, 150), Point(390, 100), "transparente", True )) #tapa izq
]

# thread setup
t = threading.Thread(target=iluminacionTotal)  # f being the function that tells how the ball should move
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
