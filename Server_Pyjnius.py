import numpy as np
import pickle
import socket
import os
#import face_recognition
import os
import pickle


# Creating Common Connection Settings for all Connection made in this script.
IP = "192.168.43.205"
Port = 1998

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, Port))

#Resources Used:
DatabaseFile = 'dataset_faces.dat'
imageDir = "Photos/"


def SelectOp(op):
    switcher = {
        '0': "CONTINUE",
        '1': "APPEND",
        '2': "DELETE",
    }
    return (switcher.get(op, "INVALID_OP!"))


def Server():
    jump = False
    # start listening for any operations from client.
    s.listen(999)
    print("socket is listening...")

    # Always looking to connections.
    while True:
        if jump == False:
            print("Waiting for next operations...")
            clientsocket, address = s.accept()
            print("Server Connected With Client...")

            received_op = clientsocket.recv(1).decode('utf-8')
            print("Operation is : " + received_op)
            clientsocket.close()
            jump = False

        # if operation is APPEND
        if SelectOp(received_op) == "APPEND":
            print("Append-Operation is being done...")
            result = BakeFaceEncoding()

            #create connection for sending ACK
            #Warning! hide the navMenu in app until this connection successfully sends ACK
            # or closes connection otherwise it will stuck here for making a connection to send ack
            #and no one will listen in app
            s.listen(999)
            print("socket is listening...")
            CSckt, CAddress = s.accept()
            print(f"Connection from {address} has been established!")


            CSckt.sendall("?ACK\n".encode('utf-8'))
            if result == 3:
                # it means user didn't ADD any person,
                # just went to some other menu option so continue server loop
                # for listning to next operation sent by user.
                continue
            if result == -1:
                CSckt.sendall("Database-Resource is not available!\n".encode('utf-8'))
                continue
            if result == 0:
                CSckt.sendall("No Faces Found!\n".encode('utf-8'))
                jump = True
                received_op = '1'
                continue
            if result == 1:
                CSckt.sendall("Person Added Successfully.\n".encode('utf-8'))
                continue
            if result == 2:
                CSckt.sendall("Multiple Faces Found!\n".encode('utf-8'))
                jump = True
                received_op = '1'
                continue
            CSckt.close()

        # if operation is DELETE
        if SelectOp(received_op) == "DELETE":
            print("Delete-Operation is being done...")
            result = DeleteOP()

            clientsocket.sendall("?ACK\n".encode('utf-8'))
            if result == -1:
                clientsocket.sendall("Database-Resource is not available!\n".encode('utf-8'))
                continue
            if result == 1:
                clientsocket.sendall("Person Removed Successfully.\n".encode('utf-8'))
                print("Delete-Operation is done successfully.")
                continue




def DeleteOP():
    # Reading Op byte
    s.listen(999)
    print("socket is listening...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    if not SelectOp(clientsocket.recv(1).decode('utf-8')) == "CONTINUE":
        print("Rolling Back From DeleteOP!")
        return

    print("Delete-Operation is being done...")
    # Read name to delete
    s.listen(999)
    print("socket is listening...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    # reads first 2 bytes for name's length in bytes
    name_length = clientsocket.recv(2).decode()
    print("DeleteName_length is:" + name_length)
    # recieve name
    delete_name = clientsocket.recv(int(name_length)).decode()
    print("DeleteName is :" + delete_name)
    clientsocket.close()

    DeletePerson(delete_name)


def DeletePerson(name):
    with open(DatabaseFile, 'rb') as f:
        try:
            while True:
                all_face_encodings = pickle.load(f)
        except EOFError:
            return -1 #pass

    all_face_encodings.pop(name)
    print(str(all_face_encodings))

    with open(DatabaseFile, 'wb') as f1:
        pickle.dump(all_face_encodings, f1)

    return 1

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


def BakeFaceEncoding():
    name, imageFile = RecieveNamePhoto()

    #########checking for OP#############
    if (not name) or (not imageFile):
        print("Rolling Back From BackFaceEncoding!")
        return 3
    #####################################

    print(f"Backing Face-Encoding with Received photo & name.")
    dir = imageFile
    person = name

    face_encodings = {}
    face = face_recognition.load_image_file(dir)
    # calculate no. of face in sample-image
    face_bounding_boxes = face_recognition.face_locations(face)
    no_of_faces = len(face_bounding_boxes)

    if no_of_faces == 0:
        print("No Faces Found!")
        return 0
    if no_of_faces == 1:
        face_encodings[person] = face_recognition.face_encodings(face)[0]

        if not os.path.exists(DatabaseFile):
            print("DatabaseFile not found creating it...")
            os.mkdir(DatabaseFile)
        try:
            with open(DatabaseFile, 'a+') as f:
                pickle.dump(face_encodings, f)
        except IOError:
            return -1

        return 1
    else:
        print(person + "_img contains multiple faces!")
        return 2

# File Transfer
def RecieveNamePhoto():
    print("Reading Name & Photo...")
    # Reading Op byte
    s.listen(999)
    print("socket is listening...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    OPbyte = clientsocket.recv(1).decode()
    print("Recieved OpByte is: "+ OPbyte)
    if not SelectOp(str(OPbyte)) == "CONTINUE":
        return

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

    #delimter for receiving photo
    if not clientsocket.recv(6).decode() == "?image":
        return None, None
    print("Image delimeter recieved successfully.")

    if not os.path.exists(imageDir):
        print("Dir not found creating dir...")
        os.mkdir(imageDir)

    # reading photo
    length = 0
    with open(imageDir + name + ".png", 'wb') as f:
        while length < photo_length_int:
            bytes = clientsocket.recv(min(1024, (photo_length_int - length)))
            length += len(bytes)
            f.write(bytes)
    f.close()
    clientsocket.close()
    # s.close()

    imageFile = imageDir + name + ".png"
    return name, imageFile


def SendNamePhoto(name):
    s.listen(999)
    print("socket is listening...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    # send name_delimeter
    clientsocket.sendall("?name\n".encode('utf-8'))
    # send name
    name1 = name + "\n"
    print("Name was sent succesfully.")
    clientsocket.sendall(name1.encode('utf-8'))

    # send image_delimeter
    clientsocket.sendall("?start\n".encode('utf-8'))
    # send image
    imageFile = open("hand.jpg", 'rb')
    Imagecontent = imageFile.read()
    imageSize = len(Imagecontent)
    print("ImageSize is:" + str(imageSize))

    # send imageSize
    imageSize_str = str(imageSize) + "\n"
    clientsocket.sendall(imageSize_str.encode('utf-8'))
    # send imageFile_delimeter
    clientsocket.sendall("?imageFile\n".encode('utf-8'))
    clientsocket.close()

    # Creating new Connetion to send music
    s.listen(999)
    print("socket is listening...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    print("Ready to receive Image....")

    # send imageFile
    clientsocket.sendall(Imagecontent)
    print("Content type is :" + str(type(Imagecontent)))
    print("Image File Content is : " + str(Imagecontent))
    print("Image was sent succesfully.")

    # receive success ACK


# message = clientsocket.recv(2)
# if message == "ok":
#   print("ACK received.")

# RecieveNamePhoto()
# SendName("sarvesh")
Server()
