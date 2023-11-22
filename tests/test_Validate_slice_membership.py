import unittest
from regression_workbench import dataset as m


class Contract(unittest.TestCase):
    def test_slice_contract(self):
        c = {
            "id": "a",
            "task": "tool",
            "input": "hello",
            "expected": {},
            "slices": ["critical", "critical"],
        }
        with self.assertRaises(ValueError):
            m.validate({"version": 1, "name": "x", "cases": [c]})
        c["slices"] = "critical"
        with self.assertRaises(ValueError):
            m.validate({"version": 1, "name": "x", "cases": [c]})
