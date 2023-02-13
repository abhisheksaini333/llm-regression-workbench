import unittest
from regression_workbench import evaluators as m
class Contract(unittest.TestCase):
 def test_types(self):
  e={'properties':{'n':{'type':'integer'},'ok':{'type':'boolean'}}}
  self.assertEqual(m.schema('{"n":true,"ok":1}',e)['score'],0)
  self.assertEqual(m.schema('{"n":1,"ok":true}',e)['score'],1)
