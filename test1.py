import numpy as np


arr = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9]
])
print(arr)
arr = arr.tolist()
print(arr)
arr.pop(0)
print(arr)
arr = np.array(arr)
print(arr)








sin = s.getInputStream()
sout = s.getOutputStream()
inn = DataInputStream(sin)
insr = InputStreamReader(socket.getInputStream())
mBufferIn = BufferedReader(insr)

#in this while the client listens for the messages sent by the server
while True:
    mServerMessage = mBufferIn.readLine()
    if mServerMessage != null:
        # Check if data is image
        if mServerMessage.equals("?start"):
            #Get length of image byte array
            size = Integer.parseInt(mBufferIn.readLine())

            #Create buffers
            msg_buff = byte[1024]
            img_buff = byte[size]
            img_offset = 0

            while True:
                bytes_read = inn.read(msg_buff, 0, msg_buff.length)
                if bytes_read == -1:
                    break

                #copy bytes into img_buff
                System.arraycopy(msg_buff, 0, img_buff, img_offset, bytes_read)
                img_offset += bytes_read
                if img_offset >= size:
                    break

        directory =
        file = File(directory, "signal.jpeg")
        bitmap = BitmapFactory.decodeByteArray(img_buff, 0, img_buff.length)
        fos = null
        try:
            fos = FileOutputStream(file)
            # Use compress method on Bitmap object to write image to OutputStream
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, fos)
            # Send OK byte[]
            OK = {0x4F, 0x4B}
            sout.write(OK)
        except:
            print("Something Wrong with File Handling!....")
