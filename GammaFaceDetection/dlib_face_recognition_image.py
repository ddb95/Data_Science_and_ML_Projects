# The face recognition library dlib is build on top of C++. dlib is C++ toolkit which contains ML algorithms and tools for creating complex sw.

import face_recognition
from PIL import Image

image = face_recognition.load_image_file('/home/debadatta/Pictures/football.jpg')

# Try to find all the locations of all the image
face_locations = face_recognition.face_locations(image)
print('I found {} faces in the photo'.format(len(face_locations)))

# Finding exact positions of the faces of images and store a separate image folder

i = 0
# Iterating over face_locations
for face_location in face_locations:
    top, right, bottom, left = face_location
    print('Face Located at TOP: {}, Left: {}, Bottom: {}, Right: {}'.format(top, left, bottom, right))
    # Access the actual face itself
    face_image = image[top:bottom, left:right]
    # recreate an image from the face_image array
    pil_image = Image.fromarray(face_image)
    pil_image.save('faces/face-{}.jpg'.format(i))
    i = i + 1
