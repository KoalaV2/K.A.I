#!/usr/bin/env python3
import library.calculator as calculator
import library.time as time
import os
import subprocess
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    try:
        print("""Hello user! \n What\'s your name?""")
        subprocess.call(["espeak", "Hello user! What's your name?"])
        name_litsen = r.listen(source)
        name = r.recognize_google(name_litsen)

        subprocess.call(["espeak", "Welcome" + name])
        print("\n Welcome", name + "\n")
    
        print("What do you want to do today?")
        subprocess.call(["espeak", "what do you want to do today"])
        command_listen = r.listen(source)
        command = r.recognize_google(command_listen)
        
        if command == "open calculator" or command == "calculator" or command == "calc":
            print("Opening calculator now!")
            subprocess.call(["espeak", "Opening calculator now"])
            calculator.calculator()
        elif command == "show current time" or command == "time" or command == "current time":
            time.time()
        elif command == "ssh info" or command == "ssh information":
            subprocess.call("library/ssh.sh")
        else:
            print("Error, something went wrong!")
    except sr.UnknownValueError as err:
        print("Encountered an error: ", err)