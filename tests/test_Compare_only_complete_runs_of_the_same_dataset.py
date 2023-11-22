import unittest
from regression_workbench import comparison as m


class Contract(unittest.TestCase):
    def test_runs(self):
        from regression_workbench.store import Store

        self.assertTrue(hasattr(m, "compare_runs"))
        with Store(":memory:") as s:
            s.register("a", "d", {}, 0, 1)
            s.register("b", "e", {}, 0, 1)
            with self.assertRaises(ValueError):
                m.compare_runs(s, "a", "b")
