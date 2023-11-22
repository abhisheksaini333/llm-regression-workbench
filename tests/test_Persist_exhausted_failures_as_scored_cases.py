import unittest
from regression_workbench import runner as m


class Contract(unittest.TestCase):
    def test_exhausted(self):
        from regression_workbench.store import Store
        from regression_workbench.providers import RetryableError

        class Down:
            def generate(self, *a):
                raise RetryableError("down")

        d = {
            "version": 1,
            "name": "x",
            "cases": [
                {"id": "a", "task": "tool", "input": "x", "expected": {"tool": "ok"}}
            ],
        }
        with Store(":memory:") as s:
            rid = m.run(
                d,
                {"model": "down", "prompt": "{input}"},
                Down(),
                s,
                max_attempts=2,
                sleep=lambda _: None,
            )
            self.assertEqual(s.results(rid)[0]["status"], "error")
            self.assertEqual(s.results(rid)[0]["score"], 0)
            self.assertEqual(len(s.attempts(rid)), 2)
