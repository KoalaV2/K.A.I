import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tensorflow
import random
import json
import tflearn
import pickle
from gtts import gTTS
import playsound
from library.utils import say
from library import calculator
from library import time
import library.youtube_dl as youtube
from library import wikipedia_summary
from library import weather
import library.face as face_rec
import os
import subprocess
import speech_recognition as sr
import library.time
trigger = "hello"
r = sr.Recognizer()

def listen():
        with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
        try:
                return r.recognize_google(audio)
        except sr.UnknownValueError:
            return ""

with open("ml-data/intents.json") as file:
    data = json.load(file)
#print(data)
try:
    with open("ml-data/data.pickle", "rb") as f:
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
    with open("ml-data/data.pickle", "wb") as f:
        pickle.dump((words,labels,training,output),f)

net = tflearn.input_data(shape=[None, len(training[0])]) # input layer
net = tflearn.fully_connected(net, 8) # 8 neurons
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") #output layer
net = tflearn.regression(net)

model = tflearn.DNN(net)
try:
    model.load("ml-data/model.tflearn")
except:
    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=1000, batch_size=8,show_metric=True)
    model.save("ml-data/model.tflearn")

def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)
print("Beggining to listen....")

while 1:
    if listen() == trigger or input() == trigger:
        try:
            playsound.playsound('library/sounds/wake_up_noise.wav', True)
            print("identifying face....")
            face_rec.face_rec()
            username = face_rec.global_name
            greeting = time.greeting
            print(greeting(time.now.hour), f" {username}, what can I do for you?")
            say(greeting(time.now.hour) + f" {username}, what can I do for you?")
            while True:

                with sr.Microphone() as source:
                    #inp = input("You: ")
                    #if inp.lower() == "quit":
                    #    break
  
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
                    if inp in ('open calculator', 'calculator', 'calc'):
                        print("Opening calculator now!")
                        say("Opening calculator now!")
                        calculator.calculator()

                    elif inp in ('show current time','local time', 'current time', 'time'):
                        print(time.now.hour)

                    elif inp in ('SSH info', 'SSH information'):
                        subprocess.call("library/ssh.sh")

                    elif inp in ('text', 'write to a text file', 'Journal','write to text file'):
                        print("What do you want to write to the file? \n")
                        say("What do you want to write to the file?")
                        text_listen = r.listen(source)
                        text = r.recognize_google(text_listen)

                        text_file = open(f'{username}_text_file.txt', 'w')
                        text_file.write(text)

                        print("The following has been written to the file: \n \n" + text)
                        say("The following has been written to the file" + text)

                    elif inp in ('goodnight', "good night", "night"):
                        say("Goodnight " + "Going to sleep now..")
                        subprocess.call('systemctl suspend', shell=True)

                    elif inp.startswith('download') and inp.endswith('from YouTube'):
                        words2 = inp.split()
                        title = words2[1:][:-2]
                        youtube.youtube(title)

                    elif inp.startswith('find summary about') and inp.endswith('on Wikipedia'):
                        words2 = inp.split()
                        summary = words2[3:][:-2]
                        wikipedia_summary.wikipedia_summary(summary)

                    elif inp in ('help', 'show inps', 'show help'):
                        print("This is what I can do, I can show the current time, write to a text file, download a youtube video, search a wikipedia summary and be a calculator")
                        say("This is what I can do, I can show the current time, write to a text file, download a youtube video, search a wikipedia summary and be a calculator")

                    elif inp.startswith('look up weather in'):
                        words2 = inp.split()
                        city_name = words2[4:]
                        weather.weather(city_name)

                    elif inp in ('quit', 'no', 'no quit the program', 'no thank you', 'goodbye', 'bye'):
                        print("Returning to standby... Have a great day!")
                        say("Returning to standby... Have a great day!")
                        playsound.playsound('library/sounds/shutdown.mp3', True)
                        r.adjust_for_ambient_noise(source)
                        break
                    else:
                        print(resp)
                        say(resp)
                        #print("Error, something went wrong!")
                        #say("Error, something went wrong!")
                    say("Anything else?")
                    print("Anything else?")
        except sr.UnknownValueError as err:
            print("Encountered an error: ", err)
