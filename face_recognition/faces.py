import numpy as np
import cv2
import pickle
import statistics

def recognize():
    face_cascade = cv2.CascadeClassifier("face_recognition/cascades/data/haarcascade_frontalface_alt2.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("face_recognition/trainner.yml")

    labels = {"person_name": 1}
    with open("face_recognition/labels.pickle", "rb") as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}

    cap = cv2.VideoCapture(0)

    results = []
    for i in range(60):
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+h]

            id_, conf = recognizer.predict(roi_gray)
            conf = 100 - float(conf)
            #print(conf)
            if conf > 50:
                name = labels[id_]

                #print(id_)
                #print(name)
                results.append(name)

    try:
        person = statistics.mode(results)
        cap.release()
        return person
    except:
        cap.release()
        return None
