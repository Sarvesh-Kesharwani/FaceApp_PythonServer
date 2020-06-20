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

tempbytes = clientsocket.recv(photo_length_int)

print(tempbytes)
print(type(tempbytes))


# PNG data
LEFT_THUMB = (
    '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
    '\x00\x13\x00\x00\x00\x0B\x08\x06\x00\x00\x00\x9D\xD5\xB6\x3A\x00\x00\x01'
    '\x2E\x49\x44\x41\x54\x78\x9C\x95\xD2\x31\x6B\xC2\x40\x00\x05\xE0\x77\x10'
    '\x42\x09\x34\xD0\x29\x21\x82\xC9\x9C\x2E\x72\x4B\x87\x40\x50\xB9\xBF\x5B'
    '\x28\x35\xA1\xA4\x94\x76\x68\x1C\x1C\x74\xCD\x9A\xE8\x20\x0A\x12\xA5\x5A'
    '\xE4\x72\xC9\x75\x10\x6D\xDC\xCE\xF7\x03\x3E\xDE\x83\x47\xA4\x94\x68\x67'
    '\xB5\xD9\x4E\xBF\xBF\x3E\xE8\x78\x3C\x86\x6A\x3C\xCF\x43\x10\x04\x20\x6D'
    '\x6C\xB5\xD9\x4E\x93\xF8\x95\x5A\x96\x05\xC6\x98\x32\x56\x14\x05\x46\xA3'
    '\x11\xB4\x36\x14\xBD\x3C\xD3\x4E\xA7\x03\xC6\x18\x8E\xC7\x23\x9A\xA6\x51'
    '\xC2\x5C\xD7\x45\x9E\xE7\x27\xEC\x0C\x39\x8E\x03\xC6\x18\x0E\x87\x83\x32'
    '\x04\x00\xE7\x75\x1A\xE7\x7C\xF2\xF9\xFE\x46\x6D\xDB\x06\x63\x0C\xFB\xFD'
    '\x1E\x75\x5D\x2B\x43\x57\x58\xF9\xF3\xAB\xAD\xD7\x6B\x98\xA6\x09\x21\x04'
    '\x76\xBB\x1D\x84\x10\x37\x61\x86\x61\x9C\x30\x00\x70\x1C\x07\x49\x92\x80'
    '\x10\x82\x7E\xBF\x8F\xE5\x72\x79\x13\x78\x69\xF6\x70\x6F\x88\x5E\xAF\x37'
    '\x2B\xCB\x92\xC6\x71\x0C\x42\x08\xC2\x30\xC4\x7C\x3E\x57\x06\x2F\x98\xAE'
    '\xEB\x4F\xAE\xEB\x4E\x06\x83\xC1\x4C\x4A\x49\xA3\x28\x82\x94\x12\x61\x18'
    '\x2A\x37\x5B\x2C\x16\xE8\x76\xBB\xFF\x3F\xE3\x9C\x4F\x8A\xA2\xD0\xD2\x34'
    '\xA5\x59\x96\xA1\xAA\x2A\x65\xCC\xB2\x2C\x0C\x87\xC3\xEB\xD3\x9E\xC1\xAA'
    '\xAA\xEE\x38\xE7\x4A\x90\xAE\xEB\x00\x00\xDF\xF7\x1F\xFF\x00\x09\x7C\xA7'
    '\x93\xB1\xFB\xFA\x11\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82'
)

width = 500
height = 333
image = Image.frombytes("RGBA", (height, width), tempbytes )
print(type(LEFT_THUMB))
def convert_string_to_bytes(string):
    bytes = b''
    for i in string:
        bytes += struct.pack("B", ord(i))
    return bytes

stream = BytesIO(convert_string_to_bytes(LEFT_THUMB))

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