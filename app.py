import json
from flask import Flask, request, make_response
from slacker import Slacker

# write token from slack api
token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
slack = Slacker(token)

app = Flask(__name__)
@app.route("/", methods = ["GET", "POST"])
def index():
    return "Hello World";

if __name__ == "__main__":
    app.run('0.0.0.0', port=8080)
