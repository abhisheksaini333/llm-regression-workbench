import unittest, tempfile, pathlib, threading, concurrent.futures
from regression_workbench import review
from regression_workbench.store import Store


class ReviewRace(unittest.TestCase):
    def test_only_one_writer_can_update_the_same_revision(self):
        with tempfile.TemporaryDirectory() as d:
            db = pathlib.Path(d) / "r.db"
            with Store(db) as s:
                for rid in ["a", "b"]:
                    s.register(rid, "d", {}, 0, 1)
                    s.save_result(rid, "case", {"score": 1})
                review.save(s, "a", "b", "case", "reviewer", "tie")
            start = threading.Barrier(2)
            insert = threading.Barrier(2)

            def writer(preference):
                with Store(db) as s:

                    def trace(sql):
                        if sql.startswith("INSERT INTO reviews "):
                            try:
                                insert.wait(timeout=0.3)
                            except threading.BrokenBarrierError:
                                pass

                    s.connection.set_trace_callback(trace)
                    start.wait(timeout=3)
                    try:
                        review.save(
                            s,
                            "a",
                            "b",
                            "case",
                            "reviewer",
                            preference,
                            expected_revision=1,
                        )
                        return "saved"
                    except ValueError as error:
                        self.assertIn("revision conflict", str(error))
                        return "conflict"

            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(writer, ["baseline", "candidate"]))
            self.assertEqual(sorted(results), ["conflict", "saved"])
            with Store(db) as s:
                self.assertEqual(review.list_reviews(s, "a", "b")[0]["revision"], 2)
