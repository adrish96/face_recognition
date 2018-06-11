import base64
import os


with open("faces.jpg","rb") as imageFile:
    str=base64.b64encode(imageFile.read())
    print str

fh=open("img.jpg","wb")
fh.write(str.decode('base64'))
fh.close()
