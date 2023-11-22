import unittest
from tests.http_support import running, get


class Contract(unittest.TestCase):
    def test_comparison_route(self):
        with running({"critical": {"critical": {"minimum": 0.8}}}) as (base, db):
            result = get(base, "/api/compare?baseline=a&candidate=b")
            self.assertFalse(result["gate"]["passed"])
            self.assertEqual(result["cases"][0]["case_id"], "case")
            self.assertEqual(result["slices"]["critical"]["candidate"], 0)
