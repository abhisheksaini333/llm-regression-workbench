import unittest
import tempfile
from pathlib import Path
from regression_workbench.comparison import bootstrap

class MaintenanceLR06Tests(unittest.TestCase):

    def test_bootstrap_settings_are_bounded(self):
        for settings in [{'resamples': 100.5}, {'resamples': 100001}, {'confidence': True}]:
            with self.subTest(settings=settings):
                with self.assertRaises(ValueError):
                    bootstrap([0.1, 0.2], **settings)

    def test_bootstrap_observations_are_numeric(self):
        for bad in [True, '1', None]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    bootstrap([bad])
