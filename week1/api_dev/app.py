import requests
import os
from flask import Flask
import json
from utility.frozen_json import FacadeJSON
from utility.result_wrapper import add_text_element
from week1.business_dev.main import app_main


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
    with open(path, "r", encoding = "utf-8") as f:
        raw = json.load(f)

    dest = app_main(raw)['result']
    message = app_main(raw)['status']

    dict2 = {"result" : dest, "status" : message}

    return dict2



def add_text_element(body, content) :
    data = content
    for i in range(0, 5):
        if data['result'].endswith("도착"):
            body.outputs.append({
                "simpleText": {
                    "text": f"[{data['result']}] : {data['status']}"
                }
            })
        else:
            station = data['result'].split('(')[1].split('방면')[0]
            body.outputs.append({
                "simpleText": {
                    "text": f"[{data['result']}] : {data['status']}"
                }
            })

    return {
        "version": "2.0",
        "template": {
            "outputs": body.outputs
        }
    }




def __generate_response_body():
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "현재 정왕역의 열차 도착 정보를 알려드릴게요!"
                    }
                }
            ]

        }
    }




if __name__ == "__main__":

    app.run()
