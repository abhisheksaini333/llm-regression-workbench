import unittest
from regression_workbench import comparison as m


class Contract(unittest.TestCase):
    def test_budgets(self):
        self.assertTrue(hasattr(m, "operational_gate"))
        b = {"p95_ms": 100, "total_tokens": 30, "errors": 1, "usage_kinds": ["tokens"]}
        self.assertEqual(
            len(
                m.operational_gate(
                    b, {"max_p95_ms": 50, "max_tokens": 20, "max_errors": 0}
                )["failures"]
            ),
            3,
        )
        self.assertTrue(
            m.operational_gate(b, {"max_p95_ms": 100, "max_errors": 1})["passed"]
        )
