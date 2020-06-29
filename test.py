import pickle
import numpy as np

def DeletePerson(name):
    with open('dataset_faces_original.dat', 'rb') as f:
        try:
            while True:
                all_face_encodings = pickle.load(f)
        except EOFError:
            pass

    all_face_encodings.pop(name)
    print(str(all_face_encodings))

    with open('temp_dataset_faces.dat', 'wb') as f1:
        pickle.dump(all_face_encodings, f1)

    with open('temp_dataset_faces.dat', 'rb') as f2:
        try:
            while True:
                temp_face_encodings = pickle.load(f2)
                print(str(temp_face_encodings))

        except EOFError:
            pass

DeletePerson('madhavi')