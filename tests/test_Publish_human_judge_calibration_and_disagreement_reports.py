import unittest
from regression_workbench import server as m
class Contract(unittest.TestCase):
 def test_analysis(self):
  from tests.http_support import running,post,get
  with running() as (base,db):
   post(base,'/api/reviews',{'baseline':'a','candidate':'b','case_id':'case','reviewer':'ana','choice':'tie','revision':0})
   report=get(base,'/api/review-analysis?baseline=a&candidate=b')
   self.assertEqual(report['reviewed'],1);self.assertEqual(report['agreement'],0)
