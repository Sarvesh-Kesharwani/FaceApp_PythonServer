import socket
import io
import struct

from PIL import Image
import bitmap
import numpy as np
from jnius import autoclass
import sys
from io import StringIO
from io import BytesIO

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
############################################################1st python's socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.43.215", 1234))
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

#reading photo length
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
print("Photo_length is :"+photo_length_string)
clientsocket.close()
#s.close()



################################################################3rd python's socket connection.
s.listen(999)
print("socket is listening...")
clientsocket, address = s.accept()
print(f"Connection from {address} has been established!")

i=1
tempbytes = []
while i != 194:
    tempbytes.append(clientsocket.recv(259))
    i += 1
#print(tempbytes)
tempbytesarray = np.array(tempbytes)
print(tempbytesarray)
print(type(tempbytesarray))
#print(type(tempbytes))

def convert_string_to_bytes(string):
    bytes = b''
    for i in string:
        bytes += struct.pack("B", ord(i))
    return bytes

stream = BytesIO(tempbytesarray)
#stream = BytesIO(convert_string_to_bytes(tempbytes))

image = Image.open(stream).convert("RGBA")
stream.close()
image.save('out.png')







'''
#################################################################################1st pyjnius socket connection.
#photo length is available in photo_length_int var.
#Reading Photo in Pyjnius

#making connection
HOST = "192.168.43.205"
Port = 1234

server = ServerSocket(Port)
System.out.println("Server started")
System.out.println("Waiting for a client ...")
socket = server.accept()
print("Client accepted")
#connection made

#pouring connection input stream into datainputstream
bis = BIS(socket.getInputStream())
dos = DOS(bis)
#Reading photo from dataipnutstream
bytesRead = 0
length = 0
buffer = []
buffer_length = 8192
baos = BAOS()

print("Reading Photo From Stream...")
while length < photo_length_int:
    bytesRead = dos.read(buffer, 0, int(Math.min(buffer_length, photo_length_int-length)))
    length += bytesRead
    #baos.write(buffer, 0, bytesRead)
    print("...")

byteArray = baos.toByteArray()
fileName = "MyFirstReceivedFile"
file = File(fileName+str(Math.random()*500)+".jpg")
if not file:
    file.createNewFile()

fos = FileOutputStream(file)
fos.write(byteArray)
fos.close()
print("Image Received")
s.close()


'''