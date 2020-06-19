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
Math = autoclass("java.lang.Math")
File = autoclass("java.io.File")
FileOutputStream = autoclass("java.io.FileOutputStream")
InputStream = autoclass("java.io.InputStream")
BufferedReader = autoclass("java.io.BufferedReader")
InputStreamReader = autoclass("java.io.InputStreamReader")


HOST = "192.168.43.215"
Port = 1234

server = ServerSocket(Port)
System.out.println("Server started")
System.out.println("Waiting for a client ...")
s = server.accept()
print("Client accepted")

bis = BIS(s.getInputStream())
inn = DOS(bis)

isr = InputStreamReader(s.getInputStream())
br = BufferedReader(isr)
#reading name_length
buff = []
while True:
    br.read(buff, 0, 1)
    if buff != "$":
        print(buff)
    else:
        break
name_length = np.array(buff)
print(name_length.tostring())
#reading name
name = []
inn.read(name, 0, name_length)
name_string = np.array(name)
print(name_string)

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


