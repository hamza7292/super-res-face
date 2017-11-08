# import image manipulation capability
from PIL import Image
# import number manipulation ability
# used for high throughput array manipulation
import numpy as np
# import scientific functionality
import scipy
# import neural network capability
# used for face recognition
import dlib
# import computer vision library
import cv2

# try/catch for importing recognition models
try:
    # trained models for face recognition capability
    import face_recognition_models
# raise exception when any error occurs
except:
    # output error message to terminal
    print('Face recognition models not importable')
    # exit program if model cannot be imported
    quit()
# dlib.get_frontal_face_detector returns object_detector
# configured for human faces that are looking at the camera
# created using scan_fhog_pyramid
# linear classifier slides over hog pyramid
face_detector = dlib.get_frontal_face_detector()
# model used by the face_recognition package
# also created by the owner of the face_recognition library
# predictor_68_point_model estimates pose of face
# points are the corner of the mouth, along the eyebrows, on the eyes...
predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
# shape_predictor takes image region and outputs set of
# point locations that define pose of an object
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)
# wrapper function to call location of face landmarks data in models folder
face_recognition_model = face_recognition_models.face_recognition_model_location()
# maps human faces to 128D vectors where pictures of same person
# mapped near each other and pictures of different people
# mapped far apart, is a .dat.bz file
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)

# encoding face
def encode_face(face_image):
    '''
        takes face image, encodes with hog
        maps human face to 128D vectors
    '''
    # creates object_detector with histogram of oriented gradients
    face_locations = face_detector(face_image,1)
    # identifies the important facial landmarks such as
    # corners mouth and eyes, tips of nose, etc...
    # for each face in one image of faces
    raw_landmarks = [pose_predictor_68_point(face_image, face_location) for face_location in face_locations]
    # encoding is 128D vector where picture of person of choice
    # mapped near to each other, and different people far apart
    # face recognition model loaded from file
    encode = [np.array(face_encoder.compute_face_descriptor(face_image,raw_landmark_set,1)) for raw_landmark_set in raw_landmarks]
    # return both the vector encoding of locations and face locations
    return encode,face_locations


def recognize_face(face_encodings,face_to_compare):
    '''
        determines if ground face_encoded is same as
        the unknown face_to_compare
    '''
    # the cutoff above which the difference between
    # ground and unknown encodings indicates a match
    tolerance = 0.6
    # difference between ground and comparison encodings
    # normal is square root of sum of squares of matrix element
    # ie magnitude of difference between the encodings
    distance = np.linalg.norm(face_encodings-face_to_compare,axis=1)
    # returns boolean list of whether differernces between
    # encodings is greater than preselected threshold
    return list(distance <= tolerance)




# end of dlib