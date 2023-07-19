import unittest
from regression_workbench import runner
from regression_workbench.providers import FixtureProvider
class Contract(unittest.TestCase):
 def test_changed_outputs(self):
  self.assertTrue(hasattr(runner,'run_key'))
  d={'version':1,'name':'x','cases':[]};c={'model':'f','prompt':'{input}'}
  self.assertNotEqual(runner.run_key(d,c,FixtureProvider({'a':'one'})),runner.run_key(d,c,FixtureProvider({'a':'two'})))
