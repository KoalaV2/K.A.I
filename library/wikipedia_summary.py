from library.utils import say
import speech_recognition as sr 
import wikipedia
from wikipedia import summary
r = sr.Recognizer()
def wikipedia_summary():
    with sr.Microphone() as source:
        say("What do you want to search for?")
        print("What do you want to search for?")
        wikipedia_article_listen = r.listen(source)
        wikipedia_article = r.recognize_google(wikipedia_article_listen)
        print(wikipedia.summary(wikipedia_article))
        say(wikipedia.summary(wikipedia_article))
