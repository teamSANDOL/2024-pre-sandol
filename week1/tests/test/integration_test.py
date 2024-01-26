# if __name__ == '__main__':
#     from sys import path
#     import os
#
#     path.append(os.path.dirname(__file__))

import os
from week1.business_dev.main import app_main
from unittest import TestCase
import json

TEST_JSON_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "../..",
    "resource",
    "RAWSubwayArrival.json"
)


class Test(TestCase):
    def setUp(self):
        with open(TEST_JSON_PATH, "r") as f:
            self.given_data = json.load(f)

    def test_app_main(self):
        given = app_main(self.given_data)["result"]
        self.assertEqual(list(given.keys()),
                         ['당고개행 - 신길온천방면', '왕십리행 - 신길온천방면', '오이도행 - 오이도방면', '인천행 - 오이도방면'])

    def test_status_code(self):
        test_json = {"status": 500, "code": "INFO-200", "message": "해당하는 데이터가 없습니다.", "link": "",
                     "developerMessage": "", "total": 0}

        given = app_main(test_json)
        self.assertEquals(given['status'], "[Error] 데이터를 받아오지 못했습니다.")

"""
- 고민한 부분 & 공부해야 할 부분- 
1. api를 따옴에 있어 사용할 url과 코드로 어떻게 끌어오는지에 대해
2. 깃허브에 대해 친숙해져야... pull/push개념과 branch와 merge에 등등 대해..
3. 코드를 짜보긴 했으나 어디에 넣어야 할지, 프로젝트의 구조와 깃허브에서 test, main에 대한 구분..
4. 기존 status데이터와 요청한 데이터들과의 비교..? api로 실시간 정보를 따왔을 때 사용자가 요청한 정보와 비교하여 맞으면 정상출력 무엇인가 오류가 나면 오류메시지 등..


"""