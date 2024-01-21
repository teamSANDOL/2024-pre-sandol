import json
import requests
FILE_PATH = r"http://swopenapi.seoul.go.kr/api/subway/sample/json/realtimeStationArrival/0/5/%EC%A0%95%EC%99%95"


def load_data() -> json:
    try:
        req = requests.get(FILE_PATH)
        result = req.text
    except FileNotFoundError:
        result = "{\"error\" :\"" + FILE_PATH + "\"}"

    return json.loads(result)


if __name__ == "__main__":
    print(load_data())