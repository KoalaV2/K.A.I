from library.utils import say
import speech_recognition as sr 
import subprocess
import webbrowser
r = sr.Recognizer()
command = 'youtube-dl "ytsearch1:'
def youtube():
    with sr.Microphone() as source:
        say("What is the title of the youtube video?")
        print("What is the title of the youtube video?")
        title_listen = r.listen(source)
        title = r.recognize_google(title_listen)
        say("What name do you want the file to have?")
        print("What name do you want the file to have?")
        file_listen = r.listen(source)
        file_name = r.recognize_google(file_listen)
        print("Searching and downloading:" + title)
        say("searching and downloading" + title)
        subprocess.call(f'youtube-dl "ytsearch1:{title}" --output "{file_name}"', shell=True)
        say(title + "has successfully been downloaded.")
        print(title + "has successfully been downloaded. \n")
        say("Do you want to play the file?")
        print("Do you want to play the file?")
        play_file_listen = r.listen(source)
        play_file = r.recognize_google(play_file_listen)
        if play_file == "yes" or "Yes":
            webbrowser.open(f"{file_name}.mkv")

        elif play_file == "no":
            pass