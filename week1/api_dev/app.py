import requests
import os
from flask import Flask
import json
from utility.frozen_json import FacadeJSON
from utility.result_wrapper import add_text_element
app = Flask(__name__)



@app.route('/')
def root():
    return "error"


@app.route('/subway')
def subway_info():
    body = __generate_response_body()
    content = __load_json(PATH)
    add_text_element(body, content)
    return add_text_element(body, content)


PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "..",
    "resource",
    "SubwayArrival.json"
)


def __load_json(path):
    with open(path, "r") as f:
        raw = json.load(f)

    return raw


def __generate_response_body():
    return {
        "version": "2.0",
        "template": {
            "outputs": [
            ]
        }
    }


if __name__ == "__main__":
    app.run()
