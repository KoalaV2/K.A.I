import pyttsx3

def say(string):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.say(string)
    engine.runAndWait()