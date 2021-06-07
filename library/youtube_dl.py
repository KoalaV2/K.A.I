from library.utils import listen
from library.utils import say
import speech_recognition as sr
import subprocess
import webbrowser
import cv2
r = sr.Recognizer()
inp = 'youtube-dl "ytsearch1:'
def youtube(title):
        say("What name do you want the file to have?")
        file_name = listen()
        say("searching and downloading" + ' '.join(title))
        subprocess.call(f'youtube-dl "ytsearch1:{title}" --output "{file_name}"', shell=True)
        say(' '.join(title) + "has successfully been downloaded.")
        say("Do you want to play the file?")
        play_file = listen()
        # TODO: Fix this cause if you say no it still plays.
        if play_file == "yes" or "Yes":
            cap = cv2.VideoCapture(f"{file_name}.mkv")
            ret, frame = cap.read()
            while(1):
              ret, frame = cap.read()
              cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
              cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
              cv2.imshow("window", frame)
              if cv2.waitKey(1) & 0xFF == ord('q') or ret==False :
                  cap.release()
                  cv2.destroyAllWindows()
                  break
              cv2.imshow('frame',frame)
        else:
            pass
