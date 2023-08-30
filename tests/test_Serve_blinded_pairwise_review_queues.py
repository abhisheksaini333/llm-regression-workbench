import unittest
from regression_workbench import server as m
class Contract(unittest.TestCase):
 def test_blind_api(self):
  from tests.http_support import running,get
  with running() as (base,db):
   value=get(base,'/api/review?baseline=a&candidate=b&reviewer=ana')
   pair=value['pairs'][0]
   self.assertNotIn('baseline',pair);self.assertEqual({pair['A'],pair['B']},{'a','b'})
   self.assertEqual(pair['revision'],0)
