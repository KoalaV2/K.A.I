#!/usr/bin/env python3
import library.calculator as calculator
import library.time as time
import os
import subprocess

print("""Hello user! \n What\'s your name?""")
subprocess.call(["espeak", "Hello user! What's your name?"])
name = input("-> ")

subprocess.call(["espeak", "Welcome" + name])
print("\n Welcome", name + "\n")

subprocess.call(["espeak", "what do you want to do today"])
command = input("What do you want to do today? \n -> ")

if command == "open calculator" or command == "calculator" or command == "calc":
    # calculator.calculator()
    # This opens REPL (Read-Eval-Print-Loop)
    subprocess.call(["dotnet", "library/calculator/parsec.dll"])
    # This just prints the result of the expression passed
    # subprocess.call(["dotnet", "library/arithmetic-evaluator/parsec.dll", "1+2"])
elif command == "show current time" or command == "time" or command == "current time":
    time.time()
elif command == "ssh info" or command == "ssh information":
    subprocess.call("library/ssh.sh")
else:
    print("Error, something went wrong!")