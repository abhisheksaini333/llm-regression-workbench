import unittest
from regression_workbench.server import create_server
from regression_workbench.cli import parser
class Contract(unittest.TestCase):
 def test_bind_contract(self):
  self.assertEqual(parser().parse_args(['serve']).host,'127.0.0.1')
  self.assertEqual(parser().parse_args(['serve','--host','0.0.0.0']).host,'0.0.0.0')
  with self.assertRaises(ValueError):create_server(':memory:',host='remote.invalid')
