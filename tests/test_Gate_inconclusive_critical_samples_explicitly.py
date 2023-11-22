import unittest
from regression_workbench import comparison as m


class Contract(unittest.TestCase):
    def test_minimum_sample(self):
        c = {
            "overall": {"delta": 0},
            "slices": {
                "critical": {
                    "count": 1,
                    "candidate": 1,
                    "delta": 0,
                    "interval": {"low": -0.2},
                }
            },
        }
        g = m.gate(c, {"critical": {"min_cases": 5, "lower_delta_bound": 0}})
        self.assertFalse(g["passed"])
        self.assertEqual(len(g["failures"]), 2)
