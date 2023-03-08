import unittest
from regression_workbench import redaction as m
class Contract(unittest.TestCase):
 def test_tokens(self):
  self.assertEqual(m.redact('Authorization: Bearer abc-123'), 'Authorization: Bearer [REDACTED]')
  self.assertNotIn('sk-abcdefghijk123456',m.redact('failed sk-abcdefghijk123456'))
