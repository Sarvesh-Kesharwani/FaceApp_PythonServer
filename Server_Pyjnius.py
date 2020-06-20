import socket
import io
from PIL import Image
import bitmap
import numpy as np
from jnius import autoclass

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


#Reading name in pure python
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


#reading photo length
photo_length_list = []

while True:
    tempbyte = clientsocket.recv(1)
    print(tempbyte)
    if tempbyte != '$':
        photo_length_list.append(tempbyte)
    else:
        break
photo_length = np.array(photo_length_list)
print("Photo_length is :"+photo_length)
clientsocket.close()
s.close()
#################################################################################
#Reading Photo in Pyjnius
HOST = "192.168.43.205"
Port = 1234

server = ServerSocket(Port)
System.out.println("Server started")
System.out.println("Waiting for a client ...")
s = server.accept()
print("Client accepted")

bis = BIS(s.getInputStream())
inn = DOS(bis)
#reading photo size
#photo_length = inn.readInt()

print("Photo Size is:"+str(photo_length))
#image_array length was read in photo_length.

bytesRead = 0
buffer = []
baos = BAOS()

print("Reading Photo From Stream...")
inn.read(buffer, 0, photo_length)  #int(Math.min(len(buffer), photo_length-length)
print("Reading Complete.")
tempArray = np.array(buffer)
print("Writing Photo to Stream...")
baos.write(tempArray, 0, len(tempArray))
print("Writing Complete.")


byteArray = np.array(baos.toByteArray())
fileName = "ReceivedFile"
file = File(fileName+str(Math.random()*500)+".jpg")
if not file:
    file.createNewFile()

fos = FileOutputStream(file)
fos.write(byteArray)
fos.close()
System.out.println("Image Received")
s.close()
inn.close()


