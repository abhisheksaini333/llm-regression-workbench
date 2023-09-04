import unittest
from regression_workbench import server as m
class Contract(unittest.TestCase):
 def test_save_api(self):
  from tests.http_support import running,post,get
  with running() as (base,db):
   result=post(base,'/api/reviews',{'baseline':'a','candidate':'b','case_id':'case','reviewer':'ana','choice':'A','revision':0})
   self.assertEqual(result['revision'],1)
   self.assertTrue(get(base,'/api/review?baseline=a&candidate=b&reviewer=ana')['pairs'][0]['reviewed'])
