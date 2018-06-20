#####################################################################################
##  This will connect to the database and update the AppicantMatch_Status column.  ##
##  To do this it will access the images stored in the folders and match them      ##
##  according to their applicationID's. If the Application ID returned by the      ##
##  recogniser is the same then they are a match else they're not.                 ##
#####################################################################################


import numpy as np
import cv2
import os
import pymssql

subjects=[]
subjects.append("")
dir_names=os.listdir('training\\')        #the training photos folder
for names in dir_names:
    subjects.append(names)

def face_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade_Haar=cv2.CascadeClassifier('C:\\Users\\nic 005\\Downloads\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml')
    faces = face_cascade_Haar.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
    if(len(faces)==0):
        return None, None
    (x,y,w,h)=faces[0]
    return gray[y:y+w, x:x+h], faces[0]

def prep_training_data(path):
    print('training starting...')
    dirs=os.listdir(path)
    faces=[]
    labels=[]
    k=0
    for dir_names in dirs:
        label=k+1
        subject_dir_path= path + "/" + dir_names
        if subject_dir_path.startswith("."):
            continue
        image=cv2.imread(subject_dir_path)
        #cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
        #cv2.waitKey(100)
        face, rect = face_detection(image)
        if face is not None:
            faces.append(face)
            labels.append(int(label))
        k=k+1
    print('training ends...')
    return faces,labels


def predict(test_img):
    img=test_img.copy()
    face, rect=face_detection(img)
    label, confidence=face_recognizer.predict(face)
    return label, confidence


faces, labels = prep_training_data('training\\')     #the training data folder
print('total images',len(faces))
print('total labels',len(labels))

face_recognizer= cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))

testing_folder=os.listdir('testing\\')          #the testing data folder
for testing_photos in testing_folder:
    img=cv2.imread('testing\\'+testing_photos)
    face, rect=face_detection(img)
    if face is None:
        ###insert into table value 'N'
        print('image skipped')
        continue
    label,confidence=predict(img)
    name=subjects[label]
    if name==testing_photos:
        #insert into table value 'Y'
        print('images match')
        print('confidence of prediction for '+name+' is ',confidence)
    else:
        #insert into table value 'N'
        print('images do not match')
            
'''
test_img=cv2.imread('C:\\Users\\nic 005\\Desktop\\face_recognition\\db\\testing\\doraj.20.jpg')
predicted_img=predict(test_img)
cv2.imshow("img",predicted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
