import unittest,json
from regression_workbench import dataset,runner,comparison
from regression_workbench.store import Store
from regression_workbench.providers import FixtureProvider
from pathlib import Path
class FixtureAcceptance(unittest.TestCase):
 def test_aggregate_cannot_mask_critical_failure(self):
  data=dataset.load('fixtures/tasks-v1.json')
  with Store(':memory:') as s:
   ids=[runner.run(data,json.loads(Path(f'fixtures/{n}-config.json').read_text()),FixtureProvider(json.loads(Path(f'fixtures/{n}-outputs.json').read_text())),s) for n in ['baseline','candidate']]
   report=comparison.compare_runs(s,*ids,json.loads(Path('fixtures/gate-policy.json').read_text()))
   self.assertGreater(report['overall']['delta'],0)
   self.assertFalse(report['gate']['passed'])
   self.assertEqual(report['slices']['critical']['candidate'],0)
