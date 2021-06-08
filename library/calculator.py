import math
from library.utils import say
import speech_recognition as sr
r = sr.Recognizer()

def calculator(user_input):
    first_number = float(user_input[-3])
    operation = user_input[-2]
    second_number = float(user_input[-1])
    print(first_number)
    if operation == "+" or operation == "add" or operation == "plus":
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
    return("\n{} {} {} is {}".format(first_number, operand, second_number, result))
