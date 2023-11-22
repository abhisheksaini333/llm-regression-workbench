import unittest
from regression_workbench import review as m


class Contract(unittest.TestCase):
    def test_missing_pair(self):
        from regression_workbench.store import Store

        with Store(":memory:") as s:
            for r in ["a", "b"]:
                s.register(r, "d", {}, 0, 0)
            with self.assertRaises(ValueError):
                m.save(s, "a", "b", "missing", "u", "tie")
