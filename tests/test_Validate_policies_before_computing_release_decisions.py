import unittest
from regression_workbench import comparison as m


class Contract(unittest.TestCase):
    def test_invalid_policy_cannot_pass(self):
        from regression_workbench.store import Store

        with Store(":memory:") as s:
            for r in ["a", "b"]:
                s.register(r, "d", {}, 0, 1)
                s.claim(r, "o")
                s.save_result(r, "x", {"score": 1, "task": "tool"})
                s.finish(r, "o", "complete")
            with self.assertRaises(ValueError):
                m.compare_runs(
                    s, "a", "b", {"critical": {"x": {"minimum": float("nan")}}}
                )
