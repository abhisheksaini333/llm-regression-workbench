import unittest
from regression_workbench import runner as m
class Contract(unittest.TestCase):
 def test_limits(self):
  from regression_workbench.store import Store
  from regression_workbench.providers import FixtureProvider
  d={'version':1,'name':'x','cases':[{'id':'a','task':'tool','input':'x','expected':{}}]}
  with Store(':memory:') as s:
   for kwargs in ({'max_attempts':0},{'max_attempts':11},{'stop_after':0}):
    with self.assertRaises(ValueError): m.run(d,{'model':'f','prompt':'{input}'},FixtureProvider({}),s,**kwargs)
   self.assertEqual(s.list_runs(),[])
