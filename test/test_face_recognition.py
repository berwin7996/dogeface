from SimpleCV import *
from random import Random
from itertools import product

def distance(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**(0.5)

def random_points(size, amount):
    r = Random()
    points = []
    for i in range(amount):
        x,  y  = (r.randint(0, size[0]), r.randint(0, size[1]))
        points.append((x,y))
    return points

def evenly_distributed_points(size, amount, min_dist, max_iter=50):
    for i in range(500):
        accepting = True
        points = random_points(size, amount)
        for p1, p2 in product(points, points):
            dist = distance(p1, p2)
            if p1 != p2 and dist < min_dist:
                accepting = False
        if accepting:
            return points
    raise Exception('max iterations reached')

def apply_phrases(drawlayer, phrases, locations):
    r = Random()
    for phrase, loc in zip(phrases, locations):
        # set font to comic sans
        drawlayer.setFontSize(50)
        color = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        drawlayer.text(phrase, loc, color)
    return drawlayer

BLACK = (0,0,0)
WHITE = (255,255,255)

if __name__ == '__main__':
    doge = Image('doge.png')
    doge_mask = Image('doge_mask.png')
    doge_mask = doge_mask.binarize().invert()
    doge_size = (doge.width, doge.height)
    faces_image = Image('multiple_faces.jpg')
    faces_image = faces_image.resize(w=1000)
    image_size = (faces_image.width, faces_image.height)
    faces_image_mask = Image(image_size)
    doge_image = Image(image_size)
    faces = faces_image.findHaarFeatures('/home/porter/src/berwin7996/dogeface/test/haarcascade_frontalface_alt.xml')
    print 'Multiple Face Test'
    for f in faces:
        face_size = (f.width(), f.height())
        print 'face found at', f.coordinates(), 'length=%d, width=%d' % face_size
        doge_scaled = doge.resize(*face_size)
        doge_mask_scaled = doge_mask.resize(*face_size)
        # masked_scaled_doge = doge_scaled.applyBinaryMask(doge_mask_scaled)
        faces_image_mask_layer = faces_image_mask.getDrawingLayer()
        faces_image_mask_layer.blit(doge_mask_scaled, f.topLeftCorner())
        faces_image_mask.applyLayers()

        doge_image_layer = doge_image.getDrawingLayer()
        doge_image_layer.blit(doge_scaled.applyBinaryMask(doge_mask_scaled), f.topLeftCorner())
        doge_image.applyLayers()
        
        faces_layer = faces_image.getDrawingLayer()
        faces_layer.blit(doge_scaled, f.topLeftCorner())
        faces_image.applyLayers()
    phrases_layer = faces_image.getDrawingLayer()
    phrases = ['wow','wow','such picture','so color','wow doge face','such doge','very fluff']
    points = evenly_distributed_points(image_size, len(phrases), 100)
    apply_phrases(phrases_layer, phrases, points)
    faces_image.applyLayers()

    final_image = (faces_image)
    final_image.save("boxed_faces_image.jpg")
