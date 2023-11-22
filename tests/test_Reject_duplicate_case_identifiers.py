import unittest
from regression_workbench import dataset as m


class Contract(unittest.TestCase):
    def test_duplicates(self):
        c = {"id": "a", "task": "tool", "input": "hello", "expected": {}}
        with self.assertRaises(ValueError):
            m.validate({"version": 1, "name": "x", "cases": [c, c]})
