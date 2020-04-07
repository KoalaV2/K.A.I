#!/usr/bin/env python3
import os 
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.camera
import face_recognition
import numpy as np
from library.utils import say

def face_rec():
    pygame.camera.init()
    cam = pygame.camera.Camera("/dev/video0",(640,480))
    cam.start()
    img = cam.get_image()
    pygame.image.save(img,"filename.jpg")
    cam.stop()

    theo_image = face_recognition.load_image_file("library/images/theo.jpg")
    theo_face_encoding = face_recognition.face_encodings(theo_image)[0]

#    raghid_image = face_recognition.load_image_file(f"library/images/raghid.jpg")
#    raghid_face_encoding = face_recognition.face_encodings(raghid_image)[0]

    known_face_encodings = [
        theo_face_encoding,
        #raghid_face_encoding
    ]
    known_face_names = [
        "Theo"
 #       "Raghid"
    ]

    unknown_image = face_recognition.load_image_file("filename.jpg")

    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            say("Welcome" + name)
            print(name)
    #Removing the image file as it's not needed anymore until when it is started again
    os.remove("filename.jpg")

