import unittest
from regression_workbench import redaction as m


class Contract(unittest.TestCase):
    def test_explicit(self):
        self.assertTrue(hasattr(m, "sanitize"))
        text = "https://host/?api_key=abc&x=2 pass=my-private-value"
        clean = m.sanitize(text, ["my-private-value"])
        self.assertNotIn("abc", clean)
        self.assertNotIn("my-private-value", clean)
        self.assertIn("x=2", clean)
