#!/usr/bin/env python3

import library.calculator as calculator

print("""Hello user! \n What\'s your name?""")

name = input("-> ")

if name.lower() == "theo":
    print("Welcome Theo \n")

    command = input("What do you want to do today? ")

    if command == "open calculator" or command == "calculator" or command == "calc":
        calculator.calculator()
elif name != "theo":
    print("Acess denied")
else:
    print("Error, something went wrong!")
