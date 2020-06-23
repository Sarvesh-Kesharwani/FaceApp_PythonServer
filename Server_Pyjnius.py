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

#Reading name in pure python
############################################################1st python's socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.43.205", 1234))
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
# s.close()
################################################################3rd python's socket connection.
s.listen(999)
print("socket is listening...")
clientsocket, address = s.accept()
print(f"Connection from {address} has been established!")

sin  = s.getInputStream()
sout = s.getOutputStream()
inn = DataInputStream(sin)
insr = InputStreamReader(socket.getInputStream())
mBufferIn = BufferedReader(insr)

while True:
    mServerMessage = mBufferIn.readLine()
    if mServerMessage != null:
        # Check if data is image
        if mServerMessage.equals("?start"):
            print("?start was recieved:...")
            # Get length of image byte array
            size = Integer.parseInt(mBufferIn.readLine())
            print("new_photo_size is:"+size)
            # Create buffers
            msg_buff = byte[1024]
            img_buff = byte[photo_length_int]
            img_offset = 0
            while True:
                bytes_read = inn.read(msg_buff, 0, msg_buff.length)
                if bytes_read == -1:
                    break
                # copy bytes into img_buff
                System.arraycopy(msg_buff, 0, img_buff, img_offset, bytes_read)
                img_offset += bytes_read
                if img_offset >= photo_length_int:
                    break
            im = Image.open(StringIO(img_buff))
            im.save("recievedImage.png")


#clientsocket.close()
#s.close()

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































