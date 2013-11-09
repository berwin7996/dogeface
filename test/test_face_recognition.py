from SimpleCV import *

if __name__ == '__main__':
    sample_face = VirtualCamera('sample_face.jpg', 'image').getImage()
    faces = sample_face.findHaarFeatures('/home/porter/src/berwin7996/dogeface/test/haarcascade_frontalface_alt.xml')

    for f in faces:
        print 'face found at', f.coordinates()

    green = (0, 255, 0)
    faces.sortColorDistance(green)[0].draw(green)
    sample_face.save("green_sample_face.jpg")
