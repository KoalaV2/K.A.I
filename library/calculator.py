import math
from library.utils import say
import speech_recognition as sr 
r = sr.Recognizer()

def calculator():
    with sr.Microphone() as source:
        say("please enter the first number")
        print("Please enter the first number: ")
        first_numer_listen = r.listen(source)
        first_number = float(r.recognize_google(first_numer_listen))
        print(first_number)
        say("What operation shall be used?")
        print("What operation shall be used? ")
        operation_listen = r.listen(source)
        operation = r.recognize_google(operation_listen)
        print(operation)
        say("Please enter the second number")
        print("Please enter the second number: ")
        second_number_listen = r.listen(source)
        second_number = float(r.recognize_google(second_number_listen))
        print(second_number)


        if operation == "+" or operation == "add":
            result = first_number + second_number
            operand = "+"
        elif operation == "-" or operation == "subtract":
            result = first_number - second_number
            operand = "-"
        elif operation == "*" or operation == "multiply":
            result = first_number * second_number
            operand = "*"
        elif operation == "/" or operation == "divide":
            result = first_number / second_number
            operand = "/"
        elif operation == "pow" or operation == "power":
            result = first_number ** second_number
            operand = "to the power of"
        else:
            print("Operation not recognized, exiting to main menu...")
            return
        print("\n{} {} {} is {}".format(first_number, operand, second_number, result))
        say("\n{} {} {} is {}".format(first_number, operand, second_number, result))
