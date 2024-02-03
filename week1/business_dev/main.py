import requests
import json
#import pprint
#for bs4 import BeautifulSoup

import requests
import json

"""
json파일..? requests..?
모듈이나 라이브러리 사용법, 기본 문법들에 대한 공부 필요

API문서에 대한 이해와 데이터 처리방식, 크롤링하는 법 등에 대한 공부

코딩할때 기본 문법과 변수나 함수명 잘 지어보기. 코딩하면서도 스스로가 헷갈려하는 부분이 많았음



"""
"""
    req = requests.get(url)
    data = json.loads(req.text) # string을 dict로 변형, key값만으로 원하는 데이터 값에 접근 가능

    print(data["realtime"][0]['arvlMsg'])
    #[0]은 인덱스, api문서에서 원하는 key값 검색 가능
    #avlMsg 는 도착지만 보고싶을 때 key값 지정하기

"""

def app_main(data: dict) -> dict:
    url = r"http://data.seoul.go.kr/dataList/OA-12764/A/1/datasetView.do"
    try:
        req = requests.get(url)
        if req.status_code == 200:
            try:
                data = req.json()
                # 여기서부터 데이터 가공 및 출력 코드 추가
                result = process_subway_data(data["realtimeArrivalList"])
                return {"result": result, "status": "success"}
            except json.JSONDecodeError as e:
                return {"error": f"[Error] JSON 디코딩 오류: {str(e)}"}
        else:
            return {"error": "[Error] 데이터를 받아오지 못했습니다."}
    except requests.RequestException as e:
        return {"error": f"[Error] {str(e)}"}


def process_subway_data(subway_data):
    result = {}

    for train_info in subway_data:
        subway_line = train_info.get("trainLineNm", "")
        arrival_msg = train_info.get("arvlMsg2", "")

        if subway_line and arrival_msg:
            result[subway_line] = [arrival_msg]

    return result


if __name__ == "__main__":
    data = {}
    res = app_main(data)
    print(res)



