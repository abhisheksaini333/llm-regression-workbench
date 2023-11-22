import unittest
from regression_workbench import dataset as m


class Contract(unittest.TestCase):
    def test_diff(self):
        self.assertTrue(hasattr(m, "diff"))
        a = {"id": "a", "task": "tool", "input": "hi", "expected": {}}
        base = {"version": 1, "name": "x", "cases": [a, dict(a, id="b")]}
        other = dict(base, cases=[dict(a, input="bye"), dict(a, id="c")])
        self.assertEqual(
            m.diff(base, other), {"added": ["c"], "removed": ["b"], "changed": ["a"]}
        )
