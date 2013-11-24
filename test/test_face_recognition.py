from sys import argv, exit
from SimpleCV import *
from random import Random
from itertools import product
from collections import Counter
import string
from PIL import Image as Img
from PIL import ImageFont as ImgFont
from PIL import ImageDraw as ImgDraw


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
        font = ImgFont.truetype('comic.ttf', 80)
        color = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        drawlayer.text(loc, phrase, color, font=font)
    return drawlayer

def process_statuses(statuses):
    r = Random()
    wordcount = Counter()
    exclude = set(string.punctuation)
    trash_words = ['the', 'a', 'be', 'is', 'an', 'of', 'and', 'to', 'in', 'that', 'i', 'not', 'on', 'with', 'have', 'it', 'for', 'he', 'she', 'as', 'you', 'do', 'did', 'at', 'this']
    for status in statuses:
        for word in status.split(' '):
            word_mod = (''.join(ch for ch in word if ch not in exclude)).lower()
            if word not in trash_words:
                wordcount[word_mod] += 1
    most_common = wordcount.most_common(10)
    longest = sorted(wordcount.keys(), reverse=True, key=lambda s: len(s))[:10]
    random_words = wordcount.keys()[:]
    r.shuffle(random_words)
    print list(most_common), longest
    phrases = []
    for i in range(r.randint(5,10)):
        phrase = ""
        roll = r.randint(0,10)
        if roll < 1:
            # wow
            phrase = "wow"
        elif roll < 4:
            # random words
            index = r.randint(0, len(random_words)-1)
            phrase = random_words[index]
            del random_words[index]
        elif roll < 6:
            # longest
            index = r.randint(0, len(longest)-1)
            phrase = longest[index]
            del longest[index]
        elif roll < 8:
            # most common
            index = r.randint(0, len(most_common)-1)
            phrase = str(most_common[index][0])
            del most_common[index]
        elif roll == 10:
            phrase = 'wow'
        
        roll2 = r.randint(0, 5)
        if roll2 < 1:
            phrase = 'so ' + phrase
        elif roll2 < 2:
            phrase = 'such ' + phrase
        elif roll2 < 3:
            phrase = 'wow ' + phrase

        roll3 = r.randint(0,5)
        if roll3 == 0:
            phrase += ' wow!'

        roll4 = r.randint(0, 4)
        if roll4 < 2:
            phrase += '!'
        elif roll4 < 3:
            phrase += '!!'
        elif roll4 < 4:
            phrase += '?!'

        phrases.append(phrase)
    return phrases



BLACK = (0,0,0)
WHITE = (255,255,255)

if __name__ == '__main__':
    #if len(argv) < 2:
    #    print 'first arg must be a url'
    #    exit(12);
    #url = argv[1]
    #url = "C:\Users\Berwin\Documents\GitHub\dogeface\test"
    r = Random()
    statuses = ["ffdgfhg","fgfhgfg","hjhj hj"]
    #statuses = ["signed lease!", "apartment", "swag", "roommies","awesome", "big kid now"]
    doge = Img.open('rig_face.png')
    faces_image = Img.open('multiple_faces.jpg').convert('RGBA')
    final_image = Img.new('RGBA', faces_image.size)
    final_image.paste(faces_image, faces_image.getbbox())
    cv_faces_image = Image('multiple_faces.jpg')
    cv_image_size = (cv_faces_image.width, cv_faces_image.height)
    faces = cv_faces_image.findHaarFeatures('C:\Users\Berwin\Documents\GitHub\dogeface\\test\haarcascade_frontalface_alt.xml')
    print 'Multiple Face Test'
    count = 0
    for f in faces:
        count+=1
        print count
        face_size = (f.width(), f.height())
        print 'face found at', f.coordinates(), 'length=%d, width=%d' % face_size
        doge_scaled = doge.resize(face_size, Img.ANTIALIAS)
        if r.randint(0,1) == 0:
            doge_scaled = doge_scaled.transpose(Img.FLIP_LEFT_RIGHT)
        x, y = f.topLeftCorner()
        final_image.paste(doge_scaled, (x, y, x+f.width(), y+f.height()), mask=doge_scaled)
    draw = ImgDraw.Draw(final_image)
    # phrases = ['wow','wow','such picture','so color','wow doge face','such doge','very fluff']
    phrases = process_statuses(statuses)
    points = evenly_distributed_points(final_image.size, len(phrases), 100)
    apply_phrases(draw, phrases, points)

    final_image.save("boxed_faces_image.jpg")
