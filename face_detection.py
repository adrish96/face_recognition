import numpy
import matplotlib.pyplot as plt
import cv2

#function for detection with XML classifier and image as parameter
def face_detection(cascade, img):
    #copy of image so that it doesn't get damaged
    img_copy = img.copy()
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    #detectMultiScale returns co-ordinates of faces in image
    faces = cascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5);
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return img

#loading the XML classifiers(both Haar and LBP)
face_cascade_Haar=cv2.CascadeClassifier('C:\\Users\\nic 005\\Downloads\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml')
face_cascade_LBP=cv2.CascadeClassifier('C:\\Users\\nic 005\\Downloads\\opencv\\sources\\data\\lbpcascades\\lbpcascade_frontalface.xml')

#loading the image
img=cv2.imread('parmendra sir.JPG')

#chage parameters for different classifier
detected_img=face_detection(face_cascade_Haar, img)
#detected_img=face_detection(face_cascade_LBP, img)

#display image with face detected
cv2.imshow('img',detected_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


