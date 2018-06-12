import base64
import os

def endcode():
    with open("faces.jpg","rb") as imageFile:
        str=base64.b64encode(imageFile.read())
        print str

def decode():
    fh=open("img.jpg","wb")
    fh.write(str.decode('base64'))
    fh.close()

'''
fh=open("img.jpg","wb")
fh.write(str.decode('base64'))
fh.close()
'''
