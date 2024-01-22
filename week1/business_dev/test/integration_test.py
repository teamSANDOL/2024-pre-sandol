if __name__ == '__main__':
    from sys import path
    import os

    path.append(os.path.dirname(__file__))

from ..main import app_main
from unittest import TestCase
import json

TEST_JSON_PATH = r"week1/resource/RawSubwayArrival.json"


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