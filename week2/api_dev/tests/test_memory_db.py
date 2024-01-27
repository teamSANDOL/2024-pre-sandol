from unittest import TestCase
from ..ref.db.memory_db import MemoryDB


class TestMemoryDB(TestCase):
    def setUp(self):
        self.db = MemoryDB()

    def test_create(self):
        self.db.create(
            "산돌 분식",
            ["떡볶이", "순대", "튀김"],
            ["짜장면", "짬뽕국", "탕수육"]
        )

    def test_read(self):
        self.fail()

    def test_update(self):
        self.db.update("한공 푸드", ["ㅁㅁㅁ"], ["ㅇㅇㅇ"])

    def test_delete(self):
        self.fail()
