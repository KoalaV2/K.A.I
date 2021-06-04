#!/usr/bin/env python3
import requests, json
from library.utils import say
import speech_recognition as sr

r = sr.Recognizer()
def weather(city_name):
    api_key = "886705b4c1182eb1c69f28eb8c520e20" # if you're curious about this being public, don't worry i found it online somewhere :p

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + ''.join(city_name) + "&units=metric"

    response = requests.get(complete_url)

    x = response.json()

    if x["cod"] != "404":


        y = x["main"]


        current_temperature = y["temp"]

        #current_pressure = y["pressure"]

        #current_humidiy = y["humidity"]

        z = x["weather"]


        weather_description = z[0]["description"]
        print("It is " + str(current_temperature) + " Celsius in " + ' '.join(city_name) + " with " + str(weather_description))
        say("It is " + str(current_temperature) + " Celsius in " + ' '.join(city_name) + " with " + str(weather_description))

    else:
        print(" City Not Found ")
