import base64
image = open('faces.jpg', 'rb')
image_read = image.read()
image_64_encode = base64.encodestring(image_read)
image_64_decode = base64.decodestring(image_64_encode)
image_result = open('faces_decode.jpg', 'wb') # create a writable image and write the decoding result image_result.write(image_64_decode) 
