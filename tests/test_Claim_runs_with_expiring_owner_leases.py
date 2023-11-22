import unittest
from regression_workbench import store as m


class Contract(unittest.TestCase):
    def test_claim(self):
        with m.Store(":memory:") as s:
            s.register("r", "d", {}, 0, 1)
            self.assertTrue(hasattr(s, "claim"))
            s.claim("r", "one", 10, now=100)
            with self.assertRaises(RuntimeError):
                s.claim("r", "two", 10, now=105)
            s.claim("r", "two", 10, now=111)
            self.assertEqual(s.get_run("r")["owner"], "two")
