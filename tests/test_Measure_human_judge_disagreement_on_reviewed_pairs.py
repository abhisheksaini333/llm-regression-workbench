import unittest
from regression_workbench import review as m
class Contract(unittest.TestCase):
 def test_agreement(self):
  self.assertTrue(hasattr(m,'agreement'))
  pairs=[{'case_id':'a','delta':1},{'case_id':'b','delta':-1}]
  labels=[{'case_id':'a','preference':'baseline'},{'case_id':'b','preference':'baseline'},{'case_id':'a','preference':'skip'}]
  a=m.agreement(pairs,labels)
  self.assertEqual(a['reviewed'],2);self.assertEqual(a['agreement'],0.5)
  self.assertEqual(a['disagreements'][0]['case_id'],'a')
