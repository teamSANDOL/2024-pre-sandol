import requests
import json
#import pprint
#from bs4 import BeautifulSoup

def app_main(data: dict) -> dict:
    #url = r"http://swopenapi.seoul.go.kr/api/subway/sample/json/realtimeStationArrival/0/5/정왕"
    # req = requests.get(url)
    # data = json.loads(req.text)
    file_path = r"C:\Users\hp\Desktop\sandol\2024-pre-sandol-master-week1and2\week1\resource\RawSubwayArrival.json"
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    train, arrival = [], []
    result = {}

    for i in range(0, 5) :
        train.append(data["realtimeArrivalList"][i]['trainLineNm'])
        arrival.append(data["realtimeArrivalList"][i]['arvlMsg2'])
        #print(f"{data['realtimeArrivalList'][i]['trainLineNm']}: {data['realtimeArrivalList'][i]['arvlMsg2']}")
        # #result
        # print(data["realtimeArrivalList"][i]['trainLineNm'], end = ": ")
        # #status
        # print(data["realtimeArrivalList"][i]['arvlMsg2'], end = ", ")

    result = dict(zip(train, arrival))

    if 'result' not in data:
        status = "[Error] 데이터를 받아오지 못했습니다."
    elif not 'result':
        status = '[Error] 도착 정보가 없습니다.'
    else :
        status = data.get("errorMessage", {}).get("message")


    dict1 = {"result" : result, "status" : status}
    #print(dict1)

    return dict1

if __name__ == "__main__":
    # data = {}
    # res = app_main(data)
    file_path = r"C:\Users\hp\Desktop\sandol\2024-pre-sandol-master-week1and2\week1\resource\RawSubwayArrival.json"
    res = app_main(file_path)
