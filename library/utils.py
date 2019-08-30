import pyttsx3

def say(string):
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)
    engine.say(string)
    engine.runAndWait()