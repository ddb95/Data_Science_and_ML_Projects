FOLDERS and why are they used : ->

dataset/ : Contains our face images organized into subfolders by name.

images/ : Contains three test images that we’ll use to verify the operation of our model.

face_detection_model/ : Contains a pre-trained Caffe deep learning model provided by OpenCV to detect faces. This model detects and localizes faces in an image.

output/ : Contains my output pickle files. If you’re working with your own dataset, you can store your output files here as well. The output files include:
        1. embeddings.pickle : A serialized facial embeddings file. Embeddings have been computed for every face in the dataset and are stored in this file.

        2. le.pickle : Our label encoder. Contains the name labels for the people that our model can recognize.

        3. recognizer.pickle : Our Linear Support Vector Machine (SVM) model. This is a machine learning model rather than a deep learning model and it is responsible for actually recognizing faces.


FILES and why are they used : ->


1. extract_embeddings.py :  Responsible for using a deep learning feature extractor to generate a 128-D vector describing a face.
                            All faces in our dataset will be passed through the neural network to generate embeddings.


2. openface_nn4.small2.v1.t7 : A Torch deep learning model which produces the 128-D facial embeddings. We’ll be using this deep learning model.


3. train_model.py : Our Linear SVM model will be trained by this script.
                    We’ll detect faces, extract embeddings, and fit our SVM model to the embeddings data.


4. recognize_video.py: we’ll recognize faces in videos. We’ll detect faces, extract embeddings, and query our SVM model to determine who is in an image.
                        We’ll draw boxes around faces and annotate each box with a name.