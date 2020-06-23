from gtts import gTTS
#import playsound
import os
from  pydub.playback import play
from pydub import AudioSegment
def say(string):
    tts = gTTS(string)
    tts.save('tts-temp.mp3')
   # playsound.playsound('tts-temp.mp3', True)
    sound = AudioSegment.from_mp3('tts-temp.mp3') 
    play(sound)
    os.remove("tts-temp.mp3")
