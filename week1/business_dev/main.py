import requests
import pprint
from bs4 import BeautifulSoup
def app_main(data: dict) -> dict:
    url = r"https://www.tukorea.ac.kr/tukorea/1096/subview.do"
    req = requests.get(url)
    pprint.pprint(req.text)
    soup = BeautifulSoup(req.text, "html.parser") # soup 객체 생성, text를 받아옴
    print(soup.find("table", {"class": "board-table horizon1"}).find(""))
    #find의 요소는 tag이름과 table의 sub클래스, 그 클래스의 이름이 보더 테이블 어쩌구

if __name__ == "__main__":
    data = {}
    res = app_main(data)

# 미션은 여기까지, 다음주부터 실전...
# /Library/Python/3.9/site-packages/urllib3/__init__.py:34: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
#   warnings.warn(
# 위 에러가 왜...? /  https://github.com/urllib3/urllib3/issues/3020
# 파이썬 3.9버전? 3.12 버전?
# 깃크라켄 pull해서 업데이트하기
# 이번 과제는 새로 클론을 생성하여 받아왔음
# 웹스크래핑 강의 들으며 전체적인 방법..?에 관해 공부했음
# https://nomadcoders.co/python-for-beginners?gad_source=1&gclid=EAIaIQobChMIjojzzICyhAMVVtUWBR1pVwBJEAAYASAAEgLks_D_BwE
# requests, beautifulSoup 등등에 관해 간단히 알아보고 응용해볼 수 있었다.