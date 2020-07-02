import json
from flask import Flask, request, make_response
from slacker import Slacker

token = "xoxb-1224553073220-1219342293842-ld19jINZkxrQEDyE5zE80zJZ"
slack = Slacker(token)

app = Flask(__name__)
@app.route("/", methods = ["GET", "POST"])
def index():
    return "Hello World";

if __name__ == "__main__":
    app.run('0.0.0.0', port=8080)