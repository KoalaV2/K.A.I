#!/usr/bin/env python3

import speech_recognition as sr 
r = sr.Recognizer()
command = "r.recognoze_google(command_listen)"
with sr.Microphone() as source:
    try:
        print("speak")
        command_listen = r.listen(source)
        command = r.recognize_google(command_listen)
        print(command)
    except sr.UnknownValueError as err:
        print(err)