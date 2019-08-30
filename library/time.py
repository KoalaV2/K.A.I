import pyttsx3
from datetime import datetime
from library.utils import say

def time():
    now = datetime.utcnow()
    
    current_time = now.strftime("%H:%M")

    say("The current time is " + current_time)
    print("The current time is:", current_time)
