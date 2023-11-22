import unittest
from regression_workbench import review as m


class Contract(unittest.TestCase):
    def test_blind(self):
        self.assertTrue(hasattr(m, "blind_pair"))
        p = {
            "case_id": "a",
            "baseline": {"output": "one"},
            "candidate": {"output": "two"},
        }
        b = m.blind_pair(p, "reviewer")
        self.assertEqual(b, m.blind_pair(p, "reviewer"))
        self.assertEqual({b["A"], b["B"]}, {"one", "two"})
        self.assertNotIn("baseline", b)
        self.assertNotIn("candidate", b)
        self.assertIn(m.unblind("a", "reviewer", "A"), {"baseline", "candidate"})
