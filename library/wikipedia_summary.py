from library.utils import say
import speech_recognition as sr 
import wikipedia
from wikipedia import summary
r = sr.Recognizer()
def wikipedia_summary(wikipedia_article):
    print(wikipedia.summary(wikipedia_article))
    say(wikipedia.summary(wikipedia_article))
