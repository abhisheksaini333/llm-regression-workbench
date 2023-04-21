import unittest
from regression_workbench import runner as m
class Contract(unittest.TestCase):
 def test_run(self):
  from regression_workbench.store import Store
  from regression_workbench.providers import FixtureProvider
  self.assertTrue(hasattr(m,'run'))
  d={'version':1,'name':'demo','cases':[{'id':'a','task':'tool','input':'lookup','expected':{'tool':'lookup'}}]}
  with Store(':memory:') as s:
   rid=m.run(d,{'model':'fixture','prompt':'{input}'},FixtureProvider({'a':'{"tool":"lookup"}'}),s)
   self.assertEqual(s.results(rid)[0]['score'],1)
   self.assertEqual(s.get_run(rid)['status'],'complete')
