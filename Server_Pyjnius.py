import struct

import numpy as np
from jnius import autoclass
import pickle
import socket

from numpy import byte

Socket = autoclass("java.net.Socket")
DOS = autoclass("java.io.DataInputStream")
System = autoclass("java.lang.System")
ServerSocket = autoclass("java.net.ServerSocket")
BIS = autoclass("java.io.BufferedInputStream")
BAOS = autoclass("java.io.ByteArrayOutputStream")
BAIS = autoclass("java.io.ByteArrayInputStream")
Math = autoclass("java.lang.Math")
File = autoclass("java.io.File")
FileOutputStream = autoclass("java.io.FileOutputStream")
InputStream = autoclass("java.io.InputStream")
BufferedReader = autoclass("java.io.BufferedReader")
InputStreamReader = autoclass("java.io.InputStreamReader")
Array = autoclass("java.lang.reflect.Array")
DataInputStream = autoclass("java.io.DataInputStream")
Integer = autoclass("java.lang.Integer")

#Creating Common Connection Settings for all Connection made in this script.
IP = "192.168.43.205"
Port = 1998
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, Port))

#####################################################Listning for Database_operation
#move this set of code to top most and modify app's for sending  the "op" byte first.
def SelectOp(op):
    switcher = {
        1: "APPEND",
        2: "DELETE",
    }
    return(switcher.get(op, "INVALID_OP!"))

def DeletePerson(name):

    def DeletePerson(name):
        with open('dataset_faces.dat', 'rb') as f:
            try:
                while True:
                    all_face_encodings = pickle.load(f)
            except EOFError:
                pass

        all_face_encodings.pop(name)
        print(str(all_face_encodings))

        with open('dataset_faces.dat', 'wb') as f1:
            pickle.dump(all_face_encodings, f1)

        '''
        with open('dataset_faces.dat', 'rb') as f2:
            try:
                while True:
                    temp_face_encodings = pickle.load(f2)
                    print(str(temp_face_encodings))

            except EOFError:
                pass
        '''
        # Example:
        # DeletePerson('madhavi')

def modifyDatabase(op):
    while True:
        s.listen(999)
        print("socket is listening...")
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established!")

        received_op = clientsocket.recv(1).decode()

        if SelectOp(received_op) == "APPEND":
            with open('dataset_faces.dat', 'a+') as f:
                #bake face_encoding with photo and name
                #save it into face_encoding
                #and store it using below line
                #using code in TakeSamples.py in ubuntu

                #or just append incoming face_encoding from iputerstream
                pickle.dump(face_encoding, f)

        if SelectOp(received_op) == "DELETE":
            DeletePerson()

#File Transfer
def ReciveName():
    # Reading name in pure python
    ############################################################1st python's socket connection.
    s.listen(999)
    print("socket is listening...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    # reads first 2 bytes for name's length in bytes
    name_length = clientsocket.recv(2).decode()
    print("Name_length is:" + name_length)
    # recieve name
    name = clientsocket.recv(int(name_length)).decode()
    print("Name is :" + name)
    clientsocket.close()
    ################################################################2nd python's socket connection.

def RecievePhoto():
    s.listen(999)
    print("socket is listening...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    # reading photo length
    photo_length_list = []
    while True:
        tempbyte = clientsocket.recv(1).decode()
        print(tempbyte)
        if tempbyte != '$':
            photo_length_list.append(tempbyte)
        else:
            break
    photo_length = np.array(photo_length_list)
    photo_length_string = ''.join(photo_length)
    photo_length_int = int(photo_length_string)
    print("Photo_length is :" + photo_length_string)
    clientsocket.close()
    ################################################################3rd python's socket connection.
    s.listen(999)
    print("socket is listening...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    # reading photo
    length = 0
    with open('image.png', 'wb') as f:
        while length < photo_length_int:
            bytes = clientsocket.recv(Math.min(1024, (photo_length_int - length)))
            length += len(bytes)
            f.write(bytes)
    f.close()
    clientsocket.close()
    #s.close()

def SendName(name):
    s.listen(999)
    print("socket is listening...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    #send name_delimeter
    clientsocket.sendall("?name\n".encode('utf-8'))
    #send name
    name1 = name + "\n"
    print("Name was sent succesfully.")
    clientsocket.sendall(name1.encode('utf-8'))


    #send image_delimeter
    clientsocket.sendall("?start\n".encode('utf-8'))
    #send image
    with open("sample.jpg", 'rb') as imageFile:
        content = imageFile.read()
        imageSize = len(content)
        print("ImageSize is:" + str(imageSize))

        # send imageSize
        imageSize_str = str(imageSize) + "\n"
        clientsocket.sendall(imageSize_str.encode('utf-8'))
        #send imageFile
        clientsocket.sendall(content)
        print("Image was sent succesfully.")

    #receive success ACK
    message = clientsocket.recv(2)
    if message == "ok":
        print("ACK received.")



ReciveName()
RecievePhoto()
SendName("sarvesh")










































