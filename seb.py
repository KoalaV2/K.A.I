#!/usr/bin/env python3

import library.calculator as calculator
import library.time as time
import os
print("""Hello user! \n What\'s your name?""")

name = input("-> ")

if name.lower() == "theo":
    print("Welcome Theo \n")

    command = input("What do you want to do today? ")

    if command == "open calculator" or command == "calculator" or command == "calc":
        calculator.calculator()
    elif command == "show current time" or command == "time" or command == "current time":
        time.time()
    elif command == "ssh info" or "ssh information":
        os.system("library/ssh.sh")
elif name != "theo":
    print("Acess denied")
else:
    print("Error, something went wrong!")
