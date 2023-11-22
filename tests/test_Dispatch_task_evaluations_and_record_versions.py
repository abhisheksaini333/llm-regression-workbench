import unittest
from regression_workbench import evaluators as m


class Contract(unittest.TestCase):
    def test_dispatch(self):
        self.assertTrue(hasattr(m, "evaluate"))
        e = m.evaluate(
            {"task": "tool", "expected": {"tool": "none"}}, '{"tool":"none"}'
        )
        self.assertEqual(e["score"], 1)
        self.assertEqual(e["version"], 1)
        with self.assertRaises(ValueError):
            m.evaluate({"task": "unknown"}, "")
