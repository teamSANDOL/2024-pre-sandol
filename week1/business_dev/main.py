import pprint
import requests
import json

def app_main(data: dict) -> dict:
    url = r"http://swopenapi.seoul.go.kr/api/subway/sample/json/realtimeStationArrival/0/5/%EC%A0%95%EC%99%95"
    req = requests.get(url)
    data = json.loads(req.text)["realtimeStationArrival"]
    result = {"result": {}}

    for train in data:
        result["result"][train["trainLineNm"]] = [train["arvMsg2"]]

    pprint.pprint(result)

if __name__ == "__main__":
    data = {}
    res = app_main(data)



