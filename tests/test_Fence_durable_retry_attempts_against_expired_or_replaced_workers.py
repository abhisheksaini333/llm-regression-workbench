import unittest, tempfile, pathlib, time
from regression_workbench.store import Store


class AttemptFencing(unittest.TestCase):
    def test_stale_worker_cannot_poison_a_new_retry_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            db = pathlib.Path(directory) / "r.db"
            with Store(db) as old, Store(db) as new:
                old.register("r", "d", {}, 0, 1)
                old.claim("r", "old", 1, now=time.time() - 2)
                self.assertTrue(hasattr(old, "record_owned_attempt"))
                with self.assertRaises(RuntimeError):
                    old.record_owned_attempt("r", "case", {"attempt": 999}, "old")
                new.claim("r", "new")
                with self.assertRaises(RuntimeError):
                    old.record_owned_attempt("r", "case", {"attempt": 999}, "old")
                new.record_owned_attempt("r", "case", {"attempt": 1}, "new")
                self.assertEqual([row["attempt"] for row in new.attempts("r")], [1])
