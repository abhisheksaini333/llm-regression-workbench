import unittest
import tempfile
from pathlib import Path
from regression_workbench.redaction import sanitize

class MaintenanceLR13Tests(unittest.TestCase):

    def test_url_userinfo_and_encoded_secrets_are_redacted(self):
        self.assertTrue('user:password' not in sanitize('https://user:password@example.org/a'))
        self.assertTrue('s%20ecret' not in sanitize('https://example.org/a?v=s%20ecret', ['s ecret']))
        self.assertTrue(sanitize('https://example.org/docs') == 'https://example.org/docs')
