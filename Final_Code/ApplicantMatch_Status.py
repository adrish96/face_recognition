#####################################################################################
##  This will connect to the database and update the AppicantMatch_Status column.  ##
##  To do this it will access the images stored in the folders and match them      ##
##  according to their applicationID's. If the Application ID returned by the      ##
##  recogniser is the same then they are a match else they're not.                 ##
##  Algorithms Used:                                                               ##
##  1)Haar Classifier for Face Detection                                           ##
##  2)Linear Binary Pattern Histogram(LBPH) for Face Recognition                   ##
#####################################################################################


import numpy as np
import cv2
import os
import pymssql
import datetime

counter = 0
start_time=datetime.datetime.now()

#connecting to the database
con=pymssql.connect(user='sa',password='Admin@123456789',database='IHHL_SBM',host='10.72.143.154')
cur=con.cursor()

#storing the names of the Training Dataset in an array -
#  becaouse LBPH classifier returns a label number associated with the detected image
#  we get the name of the detected image with this array and the label number
subjects=[]
subjects.append("")
dir_names=os.listdir('training_photos\\')        #the training photos folder containing around 1800 images
for names in dir_names:
    subjects.append(names)


#function for Face Detection
def face_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                      #converting image to grayscale
    face_cascade_Haar=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')    #loading the Haar Classifier
    faces = face_cascade_Haar.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)   #detecting faces in the image using the trained classifier
    if(len(faces)==0):                                                                #if no face is detected then return 'None'
        return None, None
    (x,y,w,h)=faces[0]                                                                #we assume that there is only one face in the image
    return gray[y:y+w, x:x+h], faces[0]


#function for preparing the training data
def prep_training_data(path):                                                         #the path of the training data folder is passed as parameter
    print('training starting...')
    dirs=os.listdir(path)
    faces=[]
    labels=[]                                                                         #label is mapped to each image, the recogniser will return the label (not image)
    k=0
    for dir_names in dirs:                                                            #iterating over the images present in the folder
        label=k+1
        subject_dir_path= path + "/" + dir_names
        if subject_dir_path.startswith("."):                                          #skipping system files, if any
            continue
        image=cv2.imread(subject_dir_path)
        #cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
        #cv2.waitKey(100)
        face, rect = face_detection(image)                                            
        if face is not None:                                                          #only images from training data which have a Face in it will be used for training
            faces.append(face)                                 
            labels.append(int(label))
        k=k+1
    print('training ends...')
    return faces,labels                  


#Function for Face Recognition 
def predict(test_img):                                                                #the test image is passed as parameter
    img=test_img.copy()
    face, rect=face_detection(img)
    label, confidence=face_recognizer.predict(face)                                   #we get the label of the subject the test-image is mapped to
    return label, confidence                                                          #confidence value is the truth value of prediction


faces, labels = prep_training_data('training_photos\\')     #the training-data folder
print('total images',len(faces))
print('total labels',len(labels))

face_recognizer= cv2.face.LBPHFaceRecognizer_create()                                 #Recogniser is created, we use LBPH. EigenFaces or FisherFaces can also be used.
face_recognizer.train(faces, np.array(labels))                                        #Recogniser is trained

testing_folder=os.listdir('details_ph_ii\\')          #the test-data folder

for testing_photos in testing_folder:                    
    app_id=testing_photos[:12]                                                        #if test_photos--> abcd.jpeg,  app_id= abcd
    img=cv2.imread('details_ph_ii\\'+testing_photos)                                  #reading the image sequentially
    counter = counter + 1
    print counter, app_id
    #face, rect=face_detection(img)
    cur.execute("Select BeneficiaryFound_status from ToiletFaceHisto where APPLICATION_ID='%s';"%(app_id))
    status = cur.fetchone()
                                                                                          
    if status[0] == 'N':                                                              #we skip the images where NO Face is detected 
        print "---> Skipped"
        cur.execute("Update ToiletFaceHisto SET ApplicantMatch_Status='N' where APPLICATION_ID='%s';"%(app_id))
        con.commit()
        continue

    #we predict which face is present in the testing-image
    label,confidence=predict(img)
    name=subjects[label]
    if name==testing_photos:                                                          #Only if the result and the orignal image have same name will we enter 'Y'
        #insert into table value 'Y'
        print('images match')
        cur.execute("Update ToiletFaceHisto SET ApplicantMatch_Status='Y' where APPLICATION_ID='%s';"%(app_id))
        con.commit()
        print('confidence of prediction for '+name+' is ',confidence)
    else:
        #insert into table value 'N'
        cur.execute("Update ToiletFaceHisto SET ApplicantMatch_Status='N' where APPLICATION_ID='%s';"%(app_id))
        con.commit()
        print('images do not match')

cur.close()
con.close()                                                                           #conn. to DB closed

end_time=datetime.datetime.now()
print "start_time = ", start_time
print "end_time = ", end_time
            
