import face_recognition
from PIL import Image

# my image
image = face_recognition.load_image_file('/home/debadatta/Pictures/passport.jpg')
# We'll use 2 images one among a lot of images and another single potrait
unknownImage = face_recognition.load_image_file('/home/debadatta/Pictures/miniMilitia.jpg')

# Encoding
debadatta_encoding = face_recognition.face_encodings(image)[0]
unknownImage_encoding = face_recognition.face_encodings(unknownImage)[0]

results = face_recognition.compare_faces([debadatta_encoding], unknownImage_encoding)

print(results)
