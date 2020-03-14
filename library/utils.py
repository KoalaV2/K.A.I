import pyttsx3

def say(string):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[9].id) 
    engine.setProperty('rate', 170)
    engine.say(string)
    engine.runAndWait()