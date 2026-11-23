import unittest
from main import build_status_payload


class TestAlertsService(unittest.TestCase):
    def test_payload_structure(self):
        data = build_status_payload()
        self.assertEqual(data["service"], "alerts")
        self.assertEqual(data["variant"], 7)
        self.assertEqual(data["status"], "ok")
        self.assertIn("version", data)


if __name__ == "__main__":
    unittest.main()