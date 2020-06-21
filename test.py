import pickle
import numpy as np

def DeletePerson(name):
    with open('dataset_faces.dat', 'rb') as f:
        try:
            while True:
                all_face_encodings = pickle.load(f)
        except EOFError:
            pass
    known_face_names = list(all_face_encodings.keys())
    known_face_encodings = np.array(list(all_face_encodings.values()))
    name_index = known_face_names.index(name)
    #new_known_face_encodings = np.delete(known_face_encodings, name_index)
    new_known_face_encodings = known_face_encodings.tolist()
    new_known_face_encodings.pop(name_index)
    new_known_face_encodings = np.array(new_known_face_encodings)


    print("known_face_names are: " + str(known_face_names))
    print("known_face_encodings are: " + str(known_face_encodings))
    print("new_known_face_encodings are: " + str(new_known_face_encodings))

    with open('temp_dataset_faces.dat', 'wb') as f:
        pickle.dump(new_known_face_encodings, f)

    with open('temp_dataset_faces.dat', 'rb') as f:
        try:
            while True:
                temp_face_encodings = pickle.load(f)
                temp_face_names = list(all_face_encodings.keys())
                print("temp_face_names are: " + str(temp_face_names))
        except EOFError:
            pass

DeletePerson("madhavi")