import unittest
from regression_workbench import runner as m
class Contract(unittest.TestCase):
 def test_resume(self):
  from regression_workbench.store import Store
  from regression_workbench.providers import FixtureProvider
  from regression_workbench.config import run_identity
  from regression_workbench.dataset import fingerprint
  d={'version':1,'name':'x','cases':[{'id':i,'task':'tool','input':'x','expected':{'tool':'ok'}} for i in ['a','b']]}
  c={'model':'fixture','prompt':'{input}'}
  with Store(':memory:') as s:
   p=FixtureProvider({'b':'{"tool":"ok"}'})
   bound=m.bound_config(c,p);rid=m.run_key(d,c,p);s.register(rid,fingerprint(d),bound,0,2);s.save_result(rid,'a',{'score':1})
   m.run(d,c,FixtureProvider({'b':'{"tool":"ok"}'}),s)
   self.assertEqual(len(s.results(rid)),2)
