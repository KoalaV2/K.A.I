#!/usr/bin/env python3
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.camera
import face_recognition
import numpy as np
import configparser as cp
from library.utils import say

config = cp.ConfigParser()
config.read('library/faces.cfg')
if 'faces' not in config: exit(1)

global_name = "Unkown"

def face_rec():
    global global_name
    pygame.camera.init()
    cam = pygame.camera.Camera("/dev/video0",(640,480))
    cam.start()
    img = cam.get_image()
    pygame.image.save(img,"filename.jpg")
    cam.stop()

    known_encodings = []
    known_names = []

    for name in config['faces']:
        file = config['faces'][name]
        image = face_recognition.load_image_file(file)
        encoding = face_recognition.face_encodings(image)[0]

        known_encodings.append(encoding)
        known_names.append(name)
        print("%s: %s" % (name, config['faces'][name]))

    unknown_image = face_recognition.load_image_file("filename.jpg")

    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)


    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            global_name = known_names[best_match_index]
        
    #Removing the image file as it's not needed anymore until when it is started again
    os.remove("filename.jpg")

