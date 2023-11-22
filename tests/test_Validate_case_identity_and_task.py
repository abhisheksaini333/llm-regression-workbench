import unittest
from regression_workbench import dataset as m


class Contract(unittest.TestCase):
    def test_invalid_case(self):
        for case in (
            {"id": "a", "task": "unknown", "input": "x", "expected": {}},
            {"id": "", "task": "extraction", "input": "x", "expected": {}},
            {"id": "a", "task": "summary", "input": None, "expected": {}},
        ):
            with self.assertRaises(ValueError):
                m.validate({"version": 1, "name": "x", "cases": [case]})
