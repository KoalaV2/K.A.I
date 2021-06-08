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
from library import spotify
import library.face as face_rec
import os
import subprocess
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import re
from flask import Flask, request
from library import light

app = Flask(__name__)
r = sr.Recognizer()

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



@app.route('/')
def main():
    inp = request.args['input']

    # TODO: Make usable with new server / client mode.
    if re.findall('[0-9]\S+',inp):
        inp = inp.split()
        response = calculator.calculator(inp)
        return response

    # TODO: Fix and not send notification to phone.
    elif inp.find('SSH') != -1:
        subprocess.call("library/ssh.sh")

    # TODO: Make usable with new server / client mode.
    elif inp in ('text', 'write to a text file', 'Journal','write to text file'):
        say("What do you want to write to the file? \n")
        text_listen = r.listen(source)
        text = r.recognize_google(text_listen)

        text_file = open(f'{username}_text_file.txt', 'w')
        text_file.write(text)

        say("The following has been written to the file: \n \n" + text)

    elif inp.startswith('download') and inp.endswith('from youtube'):
        words2 = inp.split()
        title = words2[1:][:-2]
        youtube.youtube(title)

    elif inp.startswith('find summary about') and inp.endswith('on wikipedia'):
        words2 = inp.split()
        summary = words2[3:][:-2]
        wikipedia_summary.wikipedia_summary(summary)

    elif inp.find('help') != -1:
        return("This is what I can do, I can show the current time, write to a text file, download a youtube video, search a wikipedia summary and be a calculator")

    elif inp.find('weather') != -1:
        print(inp.find('weather'))
        words2 = inp.split()
        city_name = words2[-1]
        weather_in_city = weather.weather(city_name)
        print(weather_in_city)
        return weather_in_city

    elif inp.find('lights') != -1 or inp.find('light') != -1:
        color2  = inp.split()
        color = str(color2[-1])
        light.setlightcolor(color)
        return("Setting the light to " + color + "...")

    elif inp.find('google') != -1:
        inp.encode("utf-8")
        print(inp)
        output = re.search('((?<=search\sfor\s)|(what)|(where)|(who)|(when)|(why)|(which)|(whose)|(how)|(is)|(can))(\w*.)*',inp).group(0)
        print(f"Doing a google search for {output}")
        response = google_query.google_search(output)
        title = response[0]['title']
        text = response[0]['text']
        stuff = title + '\n' + text
        return(stuff.encode("utf-8"))

    elif inp.startswith('play'):
        song1 = inp.split(' ', 1)[1]
        song2 = song1.replace('by ', '')
        print(song2)
        run_song = spotify.play_track(song2)
        song_name = run_song['name']
        artist_name = run_song['artists'][0]['name']
        return(f"Now playing {song_name} by {artist_name}")

    elif inp.startswith('pause'):
        spotify.pause_music()
        return("Paused the music.")

    elif inp.startswith('unpause') or inp.startswith('resume'):
        spotify.resume_music()

    elif inp.find('volume') != -1:
        if inp.find('raise') != -1:
            return("Raising the music volume")
        elif inp.find('lower') != -1:
            return("Lowering the music volume")
        else:
            return "Doing nothing."


    else:
        results = model.predict([bag_of_words(inp,words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                resp = random.choice(responses)
                return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
