import unittest
from regression_workbench import runner, dataset
from regression_workbench.providers import RetryableError
from regression_workbench.store import Store


class Contract(unittest.TestCase):
    def test_previous_attempts_count_towards_budget(self):
        class Down:
            calls = 0

            def generate(self, *args):
                self.calls += 1
                raise RetryableError("down")

        p = Down()
        d = {
            "version": 1,
            "name": "x",
            "cases": [{"id": "a", "task": "tool", "input": "x", "expected": {}}],
        }
        c = {"model": "f", "prompt": "{input}"}
        with Store(":memory:") as s:
            rid = runner.run_key(d, c, p)
            s.register(rid, dataset.fingerprint(d), runner.bound_config(c, p), 0, 1)
            s.record_attempt(rid, "a", {"attempt": 1})
            s.record_attempt(rid, "a", {"attempt": 2})
            runner.run(d, c, p, s, max_attempts=3, sleep=lambda _: None)
            self.assertEqual(p.calls, 1)
            self.assertEqual(s.results(rid)[0]["status"], "error")
