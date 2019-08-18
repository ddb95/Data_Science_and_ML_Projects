import cv2

# create a haar cascade classifier
# The cascade is just an XML file that contains the data to detect faces.
faceCascade = cv2.CascadeClassifier('/home/debadatta/.local/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_default.xml')

# Start video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # The detectMultiScale function is a general function that detects objects. Since we are calling it on the face cascade, that’s what it detects.
    # convert to grayscale video
    # scalefactor works in scaling the face(if face is near the camera, bigger it is, while if face is far from the camera, smaller it is.
    # The detection algorithm uses a moving window to detect objects. minNeighbors defines how many objects are detected near the current one before it declares the face found. minSize, meanwhile, gives the size of each window.

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
