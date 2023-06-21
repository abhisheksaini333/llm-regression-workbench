import unittest
from regression_workbench import review as m
class Contract(unittest.TestCase):
 def test_review(self):
  from regression_workbench.store import Store
  self.assertTrue(hasattr(m,'save'))
  with Store(':memory:') as s:
   for r in ['a','b']: s.register(r,'d',{},0,1);s.save_result(r,'case',{'score':1})
   m.save(s,'a','b','case','reviewer','candidate','clearer')
   self.assertEqual(m.list_reviews(s,'a','b')[0]['preference'],'candidate')
   with self.assertRaises(ValueError): m.save(s,'a','b','case','reviewer','wrong','')
