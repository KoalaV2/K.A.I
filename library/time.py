import pyttsx3
from datetime import datetime
engine = pyttsx3.init()
engine.setProperty('rate', 160)
def time():
    now = datetime.utcnow()
    
    current_time = now.strftime("%H:%M")

    engine.say("The current time is " + current_time)
    engine.runAndWait()
    print("The current time is:", current_time)
