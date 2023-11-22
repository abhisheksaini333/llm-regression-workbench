import unittest
from regression_workbench import comparison as m


class Contract(unittest.TestCase):
    def test_operational(self):
        self.assertTrue(hasattr(m, "operational"))
        r = m.operational(
            [
                {
                    "latency_ms": v,
                    "input_tokens": 2,
                    "output_tokens": 1,
                    "usage_kind": "tokens",
                    "status": "ok",
                }
                for v in [1, 2, 3, 4, 100]
            ]
        )
        self.assertEqual(r["p95_ms"], 100)
        self.assertEqual(r["total_tokens"], 15)
        self.assertEqual(r["errors"], 0)
