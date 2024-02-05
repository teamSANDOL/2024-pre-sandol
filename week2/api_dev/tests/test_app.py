import os
import json
from unittest import TestCase
from ..app import app
from ..lib.frozen_json import FacadeJSON


class Test(TestCase):
    def setUp(self):
        self.maxDiff = 2000
        self.app = app.test_client()
        self.base = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data"
        )

    def __common_request(self, path):
        with open(os.path.join(self.base, path), "r", encoding="UTF-8") as f:
            test_data = json.load(f)
            response = self.app.post('/updateMenu',
                                     data=json.dumps(test_data),
                                     content_type='application/json')

        return response

    def test_correction_response(self):
        response = self.__common_request("correction_test.json")
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEquals(
            {
                "response": {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "simpleText": {
                                    "text": "성공적으로 저장하였습니다.",
                                }
                            }
                        ]
                    }
                }
            }, response_data
        )

    def test_incorret_test(self):
        files = ["diff_botid_test.json",
                 "incorrect_store_name_test.json",
                 "permission_test.json"]

        for test_file in files:
            response = self.__common_request(test_file)
            self.assertEqual(200, response.status_code)

            response_data = FacadeJSON(json.loads(response.data.decode('utf-8')))
            result_text = response_data.response.template.to_json()["outputs"][0]["simpleText"]["text"]
            self.assertIn("[ERROR]", result_text)

    def test_result_file(self):
        with open(os.path.join(self.base, "../..", "repo", "menu.json"), "r", encoding="UTF-8") as f:
            load = json.load(f)

        with open(os.path.join(self.base, "correction_test.json"), "r", encoding="UTF-8") as rf:
            res_load = json.load(rf)

        names = [store["name"] for store in load["store"]]

        self.assertIn(res_load['action']['params']['store_name'], names)
