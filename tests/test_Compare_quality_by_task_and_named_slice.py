import unittest
from regression_workbench import comparison as m


class Contract(unittest.TestCase):
    def test_slices(self):
        self.assertTrue(hasattr(m, "compare"))
        a = [
            {"case_id": "a", "task": "tool", "slices": ["critical"], "score": 1},
            {"case_id": "b", "task": "summary", "score": 0},
        ]
        b = [dict(a[0], score=0), dict(a[1], score=1)]
        c = m.compare(a, b)
        self.assertEqual(c["overall"]["delta"], 0)
        self.assertEqual(c["slices"]["critical"]["delta"], -1)
        self.assertEqual(c["tasks"]["summary"]["candidate"], 1)
