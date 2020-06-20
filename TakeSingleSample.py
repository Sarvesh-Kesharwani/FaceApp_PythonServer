import face_recognition_models
import os
import pickle

def TakeSamples(dir,person):

    all_face_encodings = {}
    face = face_recognition.load_image_file(dir)
    #calculate no. of face in sample-image
    face_bounding_boxes = face_recognition.face_locations(face)
    no_of_faces = len(face_bounding_boxes)

    if no_of_faces == 1:
        all_face_encodings[person] = face_recognition.face_encodings(face)[0]
    else:
        print(person + "_img contains multiple faces!")

    with open('dataset_faces.dat', 'a+') as f:
        pickle.dump(all_face_encodings, f)



TakeSamples()