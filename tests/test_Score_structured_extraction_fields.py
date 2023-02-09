import unittest
from regression_workbench import evaluators as m
class Contract(unittest.TestCase):
 def test_fields(self):
  self.assertTrue(hasattr(m,'extraction'))
  self.assertEqual(m.extraction('{"name":"Ada","amount":12}',{'name':'Ada','amount':12})['score'],1)
  self.assertEqual(m.extraction('{"name":"Ada"}',{'name':'Ada','amount':12})['score'],0.5)
  self.assertEqual(m.extraction('not json',{'name':'Ada'})['score'],0)
