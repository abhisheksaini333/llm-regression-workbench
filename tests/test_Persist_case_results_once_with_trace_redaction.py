import unittest
from regression_workbench import store as m


class Contract(unittest.TestCase):
    def test_result(self):
        with m.Store(":memory:", secrets=["private-secret"]) as s:
            s.register("r", "d", {}, 0, 1)
            self.assertTrue(hasattr(s, "save_result"))
            s.save_result("r", "a", {"output": "private-secret", "score": 1})
            with self.assertRaises(ValueError):
                s.save_result("r", "a", {"output": "different"})
            raw = s.connection.execute("select payload from results").fetchone()[0]
            self.assertNotIn("private-secret", raw)
