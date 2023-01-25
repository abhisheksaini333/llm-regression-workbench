import unittest
from regression_workbench import dataset as m
class Contract(unittest.TestCase):
 def test_load(self):
  import tempfile,json,pathlib
  self.assertTrue(hasattr(m,'load'))
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/'d.json';p.write_text(json.dumps({'version':1,'name':'x','cases':[]}))
   self.assertEqual(m.load(p)['name'],'x')
