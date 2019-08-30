import pyttsx3

def say(string):
    engine = pyttsx3.init()
    engine.say(string)
    engine.runAndWait()
    