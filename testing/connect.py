import pymssql
import base64
import os
import cv2
import numpy as np


con=pymssql.connect(user='sa',password='sa@1234',database='easebizNZ',host='10.21.59.17')

cur=con.cursor()
cur.execute(" SELECT APPLICATION_ID, PHOTOGRAPH_IMG_CTYPE, PHOTOGRAPH_IMG FROM IHHL_DETAIL_IMG;")
result=cur.fetchall()
row=0

for results in result:
    if result[row][0] == None:
        print "Application No not found!"
        break
    if  result[row][2] == None:
        print row," photograph image is missing"
        row=row+1
        continue
    ext=result[row][1]
    name=result[row][0]
    if ext is None:
        ext='png'
    else:
        ext=ext[6:]
    fn=name + "." + ext
    print row, fn
    foldername='training_photos\\' + fn
    with open(foldername, "wb") as fh:
        fh.write(bytearray(result[row][2]))
    fh.close()
    row=row+1


cur.close()
con.close()
'''

print "Training images......"

def face_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade_Haar=cv2.CascadeClassifier('C:\\Users\\nic 005\\Downloads\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml')
    faces = face_cascade_Haar.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
    if(len(faces)==0): 
        return None, None
    (x,y,w,h)=faces[0]
    #cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return gray[y:y+w, x:x+h], faces[0]


def prep_training_data(path):
    dirs=os.listdir(path)
    faces=[]
    labels=[]
    k=0
    for dir_names in dirs:
        label=k+1
        if dir_names.startswith("."):
            continue
        image=cv2.imread(path+dir_names)
        #cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
        #cv2.waitKey(100)
        face, rect = face_detection(image)
        if face is not None:
            faces.append(face)
            labels.append(int(label))
        k=k+1
    return faces,labels


faces, labels = prep_training_data('training_photos\\')
print('total images', len(faces))
print('total labels',len(labels))


face_recognizer= cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))

print "training done..."


img=cv2.imread(foldername)
cv2.imshow(fn,img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''


