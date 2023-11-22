import unittest
from regression_workbench import runner as m


class Contract(unittest.TestCase):
    def test_pause(self):
        from regression_workbench.store import Store
        from regression_workbench.providers import FixtureProvider

        d = {
            "version": 1,
            "name": "x",
            "cases": [
                {"id": i, "task": "tool", "input": "x", "expected": {"tool": "ok"}}
                for i in ["a", "b"]
            ],
        }
        with Store(":memory:") as s:
            rid = m.run(
                d,
                {"model": "fixture", "prompt": "{input}"},
                FixtureProvider({"a": '{"tool":"ok"}', "b": '{"tool":"ok"}'}),
                s,
                stop_after=1,
            )
            self.assertEqual(s.get_run(rid)["status"], "paused")
            self.assertEqual(len(s.results(rid)), 1)
