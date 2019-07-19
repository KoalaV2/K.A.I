import math

def calculator():
    first_number = float(input("Please enter the first number: "))
    second_number = float(input("Please enter the second number: "))
    operation = input("What operation should be used? ")

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
