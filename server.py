#!/usr/bin/env python3
from flask import Flask, request
from library import light
app = Flask(__name__)


def test_input(color):
    light.setlightcolor(color)
    return color
@app.route('/')
def hello_world():
    name = request.args['color']
    test_input(name)
    return(name)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
