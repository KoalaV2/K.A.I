from library.utils import say
import speech_recognition as sr 
import subprocess
import webbrowser
r = sr.Recognizer()
inp = 'youtube-dl "ytsearch1:'
def youtube(title):
    with sr.Microphone() as source:
        say("What name do you want the file to have?")
        print("What name do you want the file to have?")
        file_listen = r.listen(source)
        file_name = r.recognize_google(file_listen)
        print("Searching and downloading:" + ' '.join(title))
        say("searching and downloading" + ' '.join(title))
        subprocess.call(f'youtube-dl "ytsearch1:{title}" --output "{file_name}"', shell=True)
        say(' '.join(title) + "has successfully been downloaded.")
        print(' '.join(title) + "has successfully been downloaded. \n")
        say("Do you want to play the file?")
        print("Do you want to play the file?")
        play_file_listen = r.listen(source)
        play_file = r.recognize_google(play_file_listen)
        if play_file == "yes" or "Yes":
            webbrowser.open(f"{file_name}.mkv")

        elif play_file == "no":
            pass