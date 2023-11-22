import unittest
from regression_workbench import comparison as m


class Contract(unittest.TestCase):
    def test_pair(self):
        self.assertTrue(hasattr(m, "pair"))
        a = [
            {"case_id": "a", "score": 1, "task": "tool"},
            {"case_id": "b", "score": 0, "task": "tool"},
        ]
        pairs = m.pair(a, list(reversed(a)))
        self.assertEqual([p["case_id"] for p in pairs], ["a", "b"])
        with self.assertRaises(ValueError):
            m.pair(a, a[:1])
        with self.assertRaises(ValueError):
            m.pair(a, [a[0], a[0]])
