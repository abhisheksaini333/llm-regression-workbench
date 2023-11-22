import unittest
from regression_workbench import redaction as m


class Contract(unittest.TestCase):
    def test_nested(self):
        self.assertTrue(hasattr(m, "redact"))
        value = {
            "headers": {"Authorization": "Bearer secret"},
            "nested": [{"api_key": "abc", "answer": "safe"}],
        }
        clean = m.redact(value)
        self.assertNotIn("secret", str(clean))
        self.assertNotIn("abc", str(clean))
        self.assertEqual(clean["nested"][0]["answer"], "safe")
        self.assertIn("secret", str(value))
