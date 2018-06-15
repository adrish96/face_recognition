'''
encoding and decoding an image into 'base64' encoded string
for transfering the image over a network or storing in a database
'''


import base64
import os


with open("faces.jpg","rb") as imageFile:
    str=base64.b64encode(imageFile.read())
    print str

fh=open("img.jpg","wb")
fh.write(str.decode('base64'))
fh.close()
