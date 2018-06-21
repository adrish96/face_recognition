import numpy as np
import cv2
import os

#face_cascade_Haar=cv2.CascadeClassifier('C:\\Users\\nic 005\\Downloads\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml')
#face_cascade_LBP=cv2.CascadeClassifier('C:\\Users\\nic 005\\Downloads\\opencv\\sources\\data\\lbpcascades\\lbpcascade_frontalface.xml')

subjects=["","amitabh","modi","parmendera sir","virat"]

def face_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade_Haar=cv2.CascadeClassifier('C:\\Users\\nic 005\\Downloads\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml')
    faces = face_cascade_Haar.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
    if(len(faces)==0): 
        return None, None
    (x,y,w,h)=faces[0]
    return gray[y:y+w, x:x+h], faces[0]
'''
def prep_training_data(path):
    dirs=os.listdir(path)
    faces=[]
    labels=[]
    k=0
    for dir_names in dirs:
        label=k+1
        subject_dir_path= path + "/" + dir_names
        subject_images_names= os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue
            image=cv2.imread(subject_dir_path+ "/" + image_name)
            cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
            cv2.waitKey(100)
            face, rect = face_detection(image)
            if face is not None:
                faces.append(face)
                labels.append(int(label))
        k=k+1
    return faces,labels
    '''
def prep_training_data(path):
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
        cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
        cv2.waitKey(100)
        face, rect = face_detection(image)
        if face is not None:
            faces.append(face)
            labels.append(int(label))
        k=k+1
    return faces,labels

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
 
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0, 255, 0), 2)

def predict(test_img):
    img=test_img.copy()
    face, rect=face_detection(img)
    label, confidence=face_recognizer.predict(face)
    print('confidence of prediction for '+subjects[label]+' is ',confidence)
    label_name=subjects[label]
    draw_rectangle(test_img,rect)
    draw_text(test_img, label_name, rect[0], rect[1]-5)
    ##the predicted image
    name=subjects[label]
    cv2.imshow("name",cv2.resize(test_img,(400,500)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #return test_img

def test_prediction(path):
    test_images=os.listdir(path)
    for image in test_images:
        img=cv2.imread(path+'/'+image)
        predict(img)


faces, labels = prep_training_data('testing\\training\\')
print('total images', len(faces))
print('total labels',len(labels))

face_recognizer= cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))

test_prediction('testing\\testing\\')
'''
test_img=cv2.imread('C:\\Users\\nic 005\\Desktop\\face_recognition\\db\\testing\\doraj.20.jpg')
predicted_img=predict(test_img)
cv2.imshow("img",predicted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
