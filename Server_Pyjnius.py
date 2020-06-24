import null
from PIL import Image
import numpy as np
from jnius import autoclass
from io import BytesIO
from io import StringIO
import pickle
import socket
import bitmap
import io
import sys
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
Array = autoclass("java.util.Arrays")



IP = "192.168.43.205"
Port = 1998
#Reading name in pure python
############################################################1st python's socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, Port))
s.listen(999)
print("socket is listening...")
clientsocket, address = s.accept()
print(f"Connection from {address} has been established!")

#reads first 2 bytes for name's length in bytes
name_length = clientsocket.recv(2).decode()
print("Name_length is:"+ name_length)
#recieve name
name = clientsocket.recv(int(name_length)).decode()
print("Name is :" +name)
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
#s.close()
################################################################3rd python's socket connection.
s.listen(999)
print("socket is listening...")
clientsocket, address = s.accept()
print(f"Connection from {address} has been established!")

# reading photo
Completedata = null
length = 0
with open('image.png', 'wb') as f:
    while length < photo_length_int:
        bytes = clientsocket.recv(Math.min(1024, (photo_length_int - length)))
        length += len(bytes)
        f.write(bytes)
        print("...")
f.close()





























"""

server = ServerSocket(Port)
System.out.println("Server started")
System.out.println("Waiting for a client ...")
socket = server.accept()
System.out.println("Client accepted")

sin  = socket.getInputStream()
sout = socket.getOutputStream()
dis = DataInputStream(sin)
insr = InputStreamReader(socket.getInputStream())
mBufferIn = BufferedReader(insr)

while True:
    mServerMessage = mBufferIn.readLine()
    if mServerMessage != null:
        # Check if data is image
        #print(mServerMessage)
        if mServerMessage == "?start":
            print("?start was recieved:...")
            # Get length of image byte array
            size = int(mBufferIn.readLine())
            print("new_photo_size is:"+str(size))

            # Create buffers
            # Reading photo from dataipnutstream
            bytesRead = 0
            length = 0
            buffer = []
            buffer_length = 1024
            baos = BAOS()

            print("Reading Photo From Stream...")
            print("Image is : ")
            #print(type(mBufferIn.readLine()))

            while length < photo_length_int:
                print("Remaining bytes to fetch is: " + str(Math.min(buffer_length, (photo_length_int - length))))
                bytesRead = mBufferIn.read(buffer, 0, Math.min(buffer_length, (photo_length_int - length)))
                length += bytesRead
                # baos.write(buffer, 0, bytesRead)
                print("...")

            byte1 = mBufferIn.readLine()
            byte2 = bytes(byte1, 'utf-8')
            print("byte2 type is:"+str(type(byte2)))

            fileName = "MyFirstReceivedFile"
            file = File(fileName + str(Math.random() * 500) + ".png")
            if not file:
                file.createNewFile()

            fos = FileOutputStream(file)
            fos.write(byte2)
            fos.close()
            print("Image Received")
            #im = Image.open(StringIO(img_buff))
            #im.save("recievedImage.png")
        #else:
            #print("Not equal to ?start....")
    else:
        print("message is empty....")

#socket.close()
#server.close()
"""









def recievePhoto():
    # reading photo length
    s.listen(999)
    print("socket is listening...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

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
    # s.close()

    s.listen(999)
    print("socket is listening...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    i = 1
    tempbytes = []
    while i != 194:
        tempbytes.append(clientsocket.recv(259))
        i += 1
    # print(tempbytes)
    tempbytesarray = np.array(tempbytes)
    print(tempbytesarray)
    print(type(tempbytesarray))
    # print(type(tempbytes))

    stream = BytesIO(tempbytesarray)

    image = Image.open(stream).convert("RGBA")
    stream.close()
    image.save('out.png')
    clientsocket.close()












#####################################################Listning for Database_operation
#move this set of code to top most and modify app's for sending  the "op" byte first.
def SelectOp(op):
    switcher = {
        1: "APPEND",
        2: "DELETE",
    }
    return(switcher.get(op, "INVALID_OP!"))

def DeletePerson(name):
    import pickle
    import numpy as np

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

#Example:
#DeletePerson('madhavi')


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































