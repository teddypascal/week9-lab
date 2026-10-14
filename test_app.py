import unittest

from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_fine(self):
        for query, expected in [("days=5", 1.5), ("days=5&deluxe=1", 3.0),
                                ("days=0", 0.0), ("days=30&deluxe=1", 5.0)]:
            with self.subTest(query=query):
                response = self.client.get("/fine?" + query)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), {"fee": expected})

    def test_invalid_days(self):
        for days in ["", "abc", "-1", "nan", "inf", "-inf"]:
            with self.subTest(days=days):
                response = self.client.get("/fine", query_string={"days": days})
                self.assertEqual(response.status_code, 400)
                self.assertTrue(response.get_json()["error"])

    def test_missing_days(self):
        response = self.client.get("/fine")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.get_json()["error"])
