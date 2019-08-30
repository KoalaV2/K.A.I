import math
import pyttsx3 

engine = pyttsx3.init()

def calculator():
    engine.say("please enter the first number")
    engine.runAndWait()
    first_number = float(input("Please enter the first number: "))
    engine.say("What operation shall be used?")
    operation = input("What operation shall be used? :")
    engine.say("Please enter the second number")
    second_number = float(input("Please enter the second number: "))


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
    engine.say(first_number, operand, second_number, result )
