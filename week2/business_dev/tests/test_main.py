from unittest import TestCase
try:
    from ..main import run
except ImportError:
    from week2.business_dev.main import run


class TestCrawlingInfo(TestCase):
    def test_create_result(self):
        result = run()
        self.assertIn('informations', result.keys())
        for k in result['informations']:
            for v in ['title', 'author', 'date', 'link']:
                self.assertIn(v, k)
