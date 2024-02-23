import json
import requests
import pprint


def app_main(data: dict) -> dict:
    url = r"http://swopenapi.seoul.go.kr/api/subway/sample/json/realtimeStationArrival/0/5/%EC%A0%95%EC%99%95"
    req = requests.get(url)
    data = json.loads(req.text)
    print(type(req.text))
    pprint.pprint(data['realtimeArrivalList'][0]['arvlMsg3'])


if __name__ == "__main__":
    data = {}
    res = app_main(data)
