#!/usr/bin/env python3
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import random
import json
import pickle
import tensorflow
import tflearn
from gtts import gTTS
from pydub.playback import play
from library.utils import say
from library import calculator
from library import time
import library.youtube_dl as youtube
from library import wikipedia_summary
from library import weather
from library import light
from library import google_query
import library.face as face_rec
import os
import subprocess
import speech_recognition as sr
import library.time
from pydub import AudioSegment
from pydub.playback import play
r = sr.Recognizer()

with open("settings.json") as settings_file:
    main_settings = json.load(settings_file)

trigger = main_settings['trigger']

with open("library/ml-data/intents.json") as file:
    data = json.load(file)
try:
    with open("library/ml-data/data.pickle", "rb") as f:
        words,labels,training,output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]
    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w  in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)
    training = numpy.array(training)
    output = numpy.array(output)
    with open("library/ml-data/data.pickle", "wb") as f:
        pickle.dump((words,labels,training,output),f)

net = tflearn.input_data(shape=[None, len(training[0])]) # input layer
net = tflearn.fully_connected(net, 8) # 8 neurons
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") #output layer
net = tflearn.regression(net)

model = tflearn.DNN(net)
try:
    model.load("library/ml-data/model.tflearn")
except:
    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=1000, batch_size=8,show_metric=True)
    model.save("library/ml-data/model.tflearn")

def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)

def listen():
        with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
        try:
                print(r.recognize_google(audio, show_all=True))
                return r.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
def adjust():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
    return ""

print("Beginning to listen....")

while 1:
    if listen() == trigger:
        try:
            #sound = AudioSegment.from_mp3('library/sounds/wake_up_noise.mp3')
            #play(sound)
            if main_settings["face_rec_toggle"] == True:
                print("identifying face....")
                face_rec.face_rec()
                username = face_rec.global_name
            else:
                print("Face recognition disabled, skipping...")
                username = "User"
            greeting = time.greeting
            say(greeting(time.now.hour) + f" {username}, what can I do for you?")
            while True:
                adjust()
                print("Speak now..")
                with sr.Microphone() as source:
                    inp_listen = r.listen(source)
                    inp = r.recognize_google(inp_listen)
                    results = model.predict([bag_of_words(inp,words)])
                    results_index = numpy.argmax(results)
                    tag = labels[results_index]
                    for tg in data["intents"]:
                        if tg['tag'] == tag:
                            responses = tg['responses']
                    resp = random.choice(responses)
                    print("You said: " + inp + "\n")
                    if inp.find("calculator") != -1:
                        say("Opening calculator now!")
                        calculator.calculator()

                    elif inp.find('SSH') != -1:
                        subprocess.call("library/ssh.sh")

                    elif inp in ('text', 'write to a text file', 'Journal','write to text file'):
                        say("What do you want to write to the file? \n")
                        text_listen = r.listen(source)
                        text = r.recognize_google(text_listen)

                        text_file = open(f'{username}_text_file.txt', 'w')
                        text_file.write(text)

                        say("The following has been written to the file: \n \n" + text)

                    elif inp.startswith('download') and inp.endswith('from YouTube'):
                        words2 = inp.split()
                        title = words2[1:][:-2]
                        youtube.youtube(title)

                    elif inp.startswith('find summary about') and inp.endswith('on Wikipedia'):
                        words2 = inp.split()
                        summary = words2[3:][:-2]
                        wikipedia_summary.wikipedia_summary(summary)

                    elif inp.find('help') != -1:
                        say("This is what I can do, I can show the current time, write to a text file, download a youtube video, search a wikipedia summary and be a calculator")

                    elif inp.find('weather') != -1:
                        print(inp.find('weather'))
                        words2 = inp.split()
                        city_name = words2[-1]
                        weather.weather(city_name)

                    elif inp.find('lights') != -1:
                        color2  = inp.split()
                        color = str(color2[-1])
                        light.setlightcolor(color)
                        say("Set the light to" + color)

                    elif inp.find('Google') != -1:
                        google_query2 = inp.split()
                        google_query_str = str(google_query2[-1])
                        response = google_query.google_search(google_query_str)
                        title = response[0]['title']
                        text = response[0]['text']
                        say(title)
                        say(text)

                    elif inp in ('quit', 'no', 'no quit the program', 'no thank you', 'goodbye', 'bye'):
                        say("Returning to standby... Have a great day!")
                        #shutdown_sound = AudioSegment.from_mp3('library/sounds/shutdown.mp3')
                        #play(shutdown_sound)
                        break
                    else:
                        say(resp)
                    say("Anything else?")
        except sr.UnknownValueError as err:
            print("Encountered an error: ", err)
