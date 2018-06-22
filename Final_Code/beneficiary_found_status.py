
######################################################################
##  This will access the folder->'details_ph_ii\\' and go through   ##
##  all the images sequentially and check if a face is detected in  ## 
##  them then access the databse and update the required column     ##
######################################################################


import os
import cv2
import pymssql
import numpy as np


print "Face detection......"

def face_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade_Haar=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade_Haar.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
    if(len(faces)==0): 
        return None, None
    (x,y,w,h)=faces[0]
    #cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return gray[y:y+w, x:x+h], faces[0]

def beneficiary_found_status(path):
    dirs=os.listdir(path)
    images_detected=0
    images_not_detected=0
    for dir_names in dirs:
        if dir_names.startswith("."):
            continue
        l=len(dir_names)
        image_type=dir_names[l-5:]
        if (image_type != '.jpeg'):                           #skipping images which are not jpeg type
            print "skipping file ",dir_names
            continue
        app_id=dir_names[:12]
        cur.execute("select STATE_CODE from IHHl_Detail_ph_ii where APPLICATION_ID='%s';"%(app_id))
        state_code=cur.fetchone()
        print app_id,state_code[0]
        image=cv2.imread(path+dir_names)
        face, rect = face_detection(image)
        if face is not None:
            cur.execute("INSERT into ToiletFaceHisto (APPLICATION_ID,STATE_CODE,BeneficiaryFound_Status) values ('%s',%d, 'Y');"%(app_id,state_code[0]))
            images_detected=images_detected+1
        else:
            cur.execute("INSERT into ToiletFaceHisto (APPLICATION_ID,STATE_CODE,BeneficiaryFound_Status) values ('%s',%d, 'N');"%(app_id,state_code[0]))
            images_not_detected=images_not_detected+1
    return images_detected, images_not_detected


con=pymssql.connect(user='sa',password='Admin@123456789',database='IHHL_SBM',host='10.72.143.154')
cur=con.cursor()
images_detected, images_not_detected=beneficiary_found_status('details_ph_ii\\')


print "faces detected=",images_detected
print "faces not detected=",images_not_detected


