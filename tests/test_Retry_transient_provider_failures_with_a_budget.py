import unittest
from regression_workbench import runner as m
class Contract(unittest.TestCase):
 def test_retry(self):
  from regression_workbench.store import Store
  from regression_workbench.providers import FixtureProvider,RetryableError
  class Flaky(FixtureProvider):
   calls=0
   def generate(self,*args):
    self.calls+=1
    if self.calls<3: raise RetryableError('Bearer abc unavailable')
    return super().generate(*args)
  p=Flaky({'a':'{"tool":"ok"}'})
  d={'version':1,'name':'x','cases':[{'id':'a','task':'tool','input':'x','expected':{'tool':'ok'}}]}
  with Store(':memory:') as s:
   rid=m.run(d,{'model':'fixture','prompt':'{input}'},p,s,sleep=lambda _:None)
   self.assertEqual(p.calls,3);self.assertEqual(len(s.attempts(rid)),2);self.assertNotIn('abc',str(s.attempts(rid)))
