from week1.api_dev import app
from unittest import TestCase
import json
import os

RESULT_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "testResource",
    "result_json.json"
)


class FlaskrTestCase(TestCase):
    def setUp(self):
        self.maxDiff = 3000
        self.result = None
        with open(RESULT_PATH) as f:
            self.result = f.readline()

        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_subway_endpoint(self):
        response = self.app.get('/subway')
        self.assertEqual(response.status_code, 200)
        print(response.data.decode("ascii"))
        print(str(self.result))
        self.assertEquals(json.loads(self.result), json.loads(response.data))
