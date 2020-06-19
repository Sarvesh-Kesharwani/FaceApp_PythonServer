import socket
import io
from PIL import Image


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.43.205", 1234))
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

    #revieve photo's length
    photo_length_list = []
    while True:
        temp = clientsocket.recv(1).decode()
        if temp != 'E':
            photo_length_list.append(temp)
        else:
            break

    #convert recieved 1-1 set of bytes into single string
    #which is nothing but length of photo_image
    print(str(photo_length_list))
    photo_length_string = ''.join(photo_length_list)
    print("PhotoLength is: "+photo_length_string)
    ''' 
    photo_length = clientsocket.recv(1024).decode()
    if not photo_length:
        print("Photo_length is empty!")
    else:
        print("Photo_Length is:" + photo_length)
    '''
    #now recieve photo_image
    photo_bytes = clientsocket.recv(int(photo_length_string))
    if not photo_bytes:
        print("PhotoByteArray is Empty!")
    else:
        print("Photo Image was Successfully Recieved.")
        print(photo_bytes)
        print("photobytes is of type: "+str(type(photo_bytes)))


    #convert photo bytes to image
    with open("images.jpg", "wb") as img:
        img.write(photo_bytes)
    #message = clientsocket.recv(1024).decode()
    #clientsocket.send(bytes("Welcome to the server!", "utf-8"))