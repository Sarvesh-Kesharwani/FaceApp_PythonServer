import face_recognition
import os
import pickle

def TakeSamples(dir,person):

    try:
        f = open(DatabaseFile, 'wb')
        all_face_encodings = pickle.load(f)
        print(str(type(all_face_encodings)))
    except IOError:
        print("error!")

TakeSamples()