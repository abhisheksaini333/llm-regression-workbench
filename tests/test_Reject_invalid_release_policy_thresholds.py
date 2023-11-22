import unittest
from regression_workbench import comparison as m


class Contract(unittest.TestCase):
    def test_policy(self):
        self.assertTrue(hasattr(m, "validate_policy"))
        for p in (
            {"critical": {"x": {"minimum": float("nan")}}},
            {"max_overall_regression": -1},
            {"critical": {"x": {"min_cases": 0}}},
            {"budgets": {"max_errors": -1}},
            {"critical": "bad"},
        ):
            with self.assertRaises(ValueError):
                m.validate_policy(p)
