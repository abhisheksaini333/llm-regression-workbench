import unittest
import tempfile
from pathlib import Path
from regression_workbench.store import Store
from regression_workbench.runner import run
from regression_workbench.providers import FixtureProvider

class MaintenanceLR10Tests(unittest.TestCase):

    def test_invalid_lease_never_registers_a_run(self):
        for bad in [True, float('nan'), float('inf'), -1]:
            with self.subTest(bad=bad):
                data = {'version': 1, 'name': 'd', 'cases': [{'id': 'c', 'task': 'summary', 'input': 'x', 'expected': {'keywords': ['x']}}]}
                with Store(':memory:') as store:
                    with self.assertRaises(ValueError):
                        run(data, {'model': 'm', 'prompt': '{input}'}, FixtureProvider({'c': 'x'}), store, lease_seconds=bad)
                    self.assertTrue(store.list_runs() == [])

    def test_invalid_claim_identity_and_clock(self):
        with Store(':memory:') as store:
            store.register('r', 'd', {}, 0, 1)
            with self.assertRaises(ValueError):
                store.claim('r', '', 10, now=0)
            with self.assertRaises(ValueError):
                store.claim('r', 'u', 10, now=float('nan'))
