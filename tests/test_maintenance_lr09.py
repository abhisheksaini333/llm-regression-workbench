import unittest
import tempfile
from pathlib import Path
from regression_workbench.store import Store
from regression_workbench.review import save, list_reviews

class MaintenanceLR09Tests(unittest.TestCase):

    def test_review_revision_is_a_nonnegative_integer(self):
        for bad in [False, 0.0, -1]:
            with self.subTest(bad=bad):
                with Store(':memory:') as store:
                    for run in ('a', 'b'):
                        store.register(run, 'd', {}, 0, 1)
                        store.save_result(run, 'c', {'score': 1})
                    with self.assertRaises(ValueError):
                        save(store, 'a', 'b', 'c', 'u', 'tie', expected_revision=bad)
                    self.assertTrue(list_reviews(store, 'a', 'b') == [])
