#!/usr/bin/env python3
import os
import face_recognition
import numpy as np
import configparser as cp
import cv2
from library.utils import say
import json

config = cp.ConfigParser()
config.read('library/faces.cfg')

with open("settings.json") as settings_file:
    main_settings = json.load(settings_file)

global_name = "Unknown"

def face_rec():
    if main_settings['face_rec_toggle'] == False:
        return ""
    if 'faces' not in config:
        print("no faces found in config.. exiting")
        exit(1)

    global global_name
    video_capture = cv2.VideoCapture(main_settings['video_device'])
    ret, frame = video_capture.read()

    if not ret:
        print("failed to grab frame")
        exit(1)

    rgb_frame = frame[:, :, ::-1]

    known_encodings = []
    known_names = []

    for name in config['faces']:
        file = config['faces'][name]
        print(file)
        image = face_recognition.load_image_file(file)
        encoding = face_recognition.face_encodings(image)[0]
        print(encoding)

        known_encodings.append(encoding)
        known_names.append(name)
        print(known_names)
        #print("%s: %s" % (name, config['faces'][name]))

    #unknown_image = face_recognition.load_image_file("filename.jpg")

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)


    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            global_name = known_names[best_match_index]
            print(global_name)
