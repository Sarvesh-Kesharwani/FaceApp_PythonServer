import socket
import io
from PIL import Image
import bitmap
import numpy as np
from jnius import autoclass
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.43.215", 1234))
s.listen(999)
print("socket is listening...")

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    #reads first 2 bytes for name's length in bytes
    name_length = clientsocket.recv(2).decode()
    print("Name_length is:"+ name_length)
    #recieve name
    name = clientsocket.recv(int(name_length)).decode()
    print("Name is :" +name)

    #*******************************************
    DOS = autoclass("java.io.DataOutputStream")
    
    dos = DOS(s.)
    photo_length = dos.readInt();
    print(photo_length)

