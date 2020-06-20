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

HOST = "192.168.43.205"
Port = 1234

server = ServerSocket(Port)
System.out.println("Server started")
System.out.println("Waiting for a client ...")
s = server.accept()
print("Client accepted")

bis = BIS(s.getInputStream())
inn = DOS(bis)

isr = InputStreamReader(s.getInputStream())
br = BufferedReader(isr) #use a streamreader which reads data in bytes

#reading name
innn = s.getInputStream()

buff = [1]
while True:
    innn.read(buff, 0, 1)# replace this line with code_to_read_one-one byte
    if buff != "#$":
        temp = np.array(buff)
        print(temp)
    else:
        break

name_string = np.array(buff)
print("Name is:"+name_string)

#reading photo size
photo_length = inn.readInt()
System.out.println("Got the Size")
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


