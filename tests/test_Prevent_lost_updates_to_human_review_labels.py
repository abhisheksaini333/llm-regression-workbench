import unittest
from regression_workbench import review as m


class Contract(unittest.TestCase):
    def test_revision(self):
        from regression_workbench.store import Store

        with Store(":memory:") as s:
            for r in ["a", "b"]:
                s.register(r, "d", {}, 0, 1)
                s.save_result(r, "case", {"score": 1})
            m.save(s, "a", "b", "case", "u", "tie")
            with self.assertRaises(ValueError):
                m.save(s, "a", "b", "case", "u", "candidate", expected_revision=0)
            self.assertEqual(
                m.save(s, "a", "b", "case", "u", "baseline", expected_revision=1)[
                    "revision"
                ],
                2,
            )
