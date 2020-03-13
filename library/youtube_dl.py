import pyttsx3
from library.utils import say
import speech_recognition as sr 
import pyttsx3
import subprocess
r = sr.Recognizer()
command = 'youtube-dl "ytsearch1:'
def youtube():
    with sr.Microphone() as source:
        say("What is the title of the youtube video?")
        title_listen = r.listen(source)
        title = r.recognize_google(title_listen)
        print("Searching and downloading:" + title)
        say("searching and downloading" + title)
        subprocess.call(f'youtube-dl "ytsearch1:{title}"', shell=True)


        
