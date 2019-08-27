'''
@Debadatta
    Code performs a Facial Recognition and creates a dataset of the faces

Steps/Outline
    1. Load Models either Caffe or Tensorflow Model, I chose Caffe Model as it was pretrained on a larger number of datasets.
    2. Set Threshold Value for checking minimum confidence
    3. Start Capturing video which is an alamgamation of multiple frames(Frames by Frames)
    4. Initialize frame_count as 0, and keep counting the frames as we need to check the fps
    5. net-> cv2.dnn.readNetFromTensorflow or cv2.dnn.readNetFromCaffe where we load the config files and Model files
    6. Pass the net and Current frame to detectFaceOpenCVDnn function.
    7. Get frame height, width
    8. Create a blob of the frame and pass it as input to the model
    9. Detections are generated and we check the confidence, only when confidence > conf_threshold we generate the bounding boxes
    10. Bounding boxes are appened and a rectangle is generated for the frame
    11. We measure the fps count and we put some label on the video
'''

from __future__ import division
import cv2
import time
import sys
import os

PATH = '/home/debadatta/ML_learning_Path/Data_Science_and_ML_Projects/GammaFaceDetection/opencv-face-recognition/dataset/'


def detectFaceOpenCVDnn(net, frame):
    # frame-> Current frame Fetched
    # net-> Model from Caffe or Tensorflow model
    frameOpencvDnn = frame.copy()

    # Get height and width of frame
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]

    # grab the frame dimensions and convert it to a blob
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], False, False)

    # Feed the image to model. Pass the blob through the network and obtain detections.
    # passing the blob through the deep neural net to obtain face detections
    net.setInput(blob)
    # print(blob.shape)

    # blob.shape (1, 3, 300, 300)
    detections = net.forward()

    # Initialized Bounding Boxes for face
    bboxes = []

    for i in range(detections.shape[2]):

        # detections.shape is (1, 1, 90, 7)
        confidence = detections[0, 0, i, 2]

        # Check if confidence is lower than conf_threshold, then reject the value
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            # cv2.rectangle(img, pt1, pt2, color, thickness, lineType, shift)
            # shift->Number of fractional bits in the point coordinates.
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)

    return frameOpencvDnn, bboxes


if __name__ == "__main__":

    name = input('Enter your Name')
    emp_id = input('Enter your Employee_ID')
    storeimagePath = os.path.join(PATH, emp_id)
    os.mkdir(storeimagePath)
    print('{} directory is created'.format(storeimagePath))
    # OpenCV DNN supports 2 networks.
    # 1. FP16 version of the original caffe implementation ( 5.4 MB )
    # 2. 8 bit Quantized version using Tensorflow ( 2.7 MB )
    # DNN = "TF"
    DNN = "CAFFE"
    if DNN == "CAFFE":
        modelFile = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
        configFile = "models/deploy.prototxt"
        # Reads a network model stored in Caffe model stored in models directory.
        net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
        print('Model Loaded')
    else:
        modelFile = "models/opencv_face_detector_uint8.pb"
        configFile = "models/opencv_face_detector.pbtxt"
        net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
        print('Model Loaded')

    # Set the Confidence Threshold value.
    conf_threshold = 0.5

    source = 0
    if len(sys.argv) > 1:
        source = sys.argv[1]

    time.sleep(0.5)

    # Start Capturing Video
    print('Face Detection Starts..')
    cap = cv2.VideoCapture(source)

    # cap.read() returns a bool (True/False). If frame is read correctly, it will be True. So you can check end of the video by checking this return value.
    hasFrame, frame = cap.read()
    vid_writer = cv2.VideoWriter('output-dnn-{}.avi'.format(str(source).split(".")[0]),
                                 cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 15, (frame.shape[1], frame.shape[0]))

    frame_count = 0
    tt_opencvDnn = 0
    total = 0

    while (hasFrame):
        hasFrame, frame = cap.read()
        if not hasFrame:
            break
        frame_count += 1

        t = time.time()
        # print(t)

        # returns frameOpencvDnn, bboxes from detectFaceOpenCVDnn function
        outOpencvDnn, bboxes = detectFaceOpenCVDnn(net, frame)

        tt_opencvDnn += time.time() - t

        # Calculate fps(frames per second)
        fpsOpencvDnn = frame_count / tt_opencvDnn

        # Labels for showing in the image
        label = "OpenCV DNN , FPS : {:.2f}".format(fpsOpencvDnn)

        cv2.imshow("Face Detection Comparison", outOpencvDnn)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('k'):
            p = os.path.sep.join([storeimagePath, '{}{}.png'.format(emp_id, str(total).zfill(5))])
            cv2.imwrite(p, outOpencvDnn)
            total += 1

        # vid_writer.write(outOpencvDnn)
        if frame_count == 1:
            tt_opencvDnn = 0

        elif key == ord("q"):
            break
    cv2.destroyAllWindows()
    vid_writer.release()
