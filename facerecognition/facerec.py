import numpy as np
import cv2
import pickle

face_cascade = cv2.CascadeClassifier("facerecognition/cascades/data/haarcascade_frontalface_alt2.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("facerecognition/trainner.yml")

labels = {"person_name": 1}
with open("facerecognition/labels.pickle", "rb") as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x,y,w,h) in faces:
        #print(x,y,w,h)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+h]

        id_, conf = recognizer.predict(roi_gray)
        conf = 100 - float(conf)
        print(conf)
        if conf > 50:
            print(id_)
            print(labels[id_])

        img_item = "facerecognition/my-image.png"
        cv2.imwrite(img_item, roi_gray)

        color = (196, 31, 255)
        stroke = 2
        width = x + w
        height = y + h
        cv2.rectangle(frame, (x,y), (width, height), color, stroke)

    cv2.imshow("frame", frame)
    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
