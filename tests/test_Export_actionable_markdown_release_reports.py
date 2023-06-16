import unittest
from regression_workbench import report as m
class Contract(unittest.TestCase):
 def test_markdown(self):
  self.assertTrue(hasattr(m,'markdown'))
  c={'baseline_id':'a','candidate_id':'b','overall':{'baseline':0.5,'candidate':0.8,'delta':0.3},'gate':{'passed':False,'failures':[{'slice':'critical','reason':'regressed'}]},'cases':[{'case_id':'bad','delta':-1}]}
  text=m.markdown(c)
  self.assertIn('BLOCKED',text);self.assertIn('critical',text);self.assertIn('bad',text)
