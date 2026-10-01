import unittest
import tempfile
from pathlib import Path
from regression_workbench.report import markdown

class MaintenanceLR15Tests(unittest.TestCase):

    def test_report_labels_cannot_inject_markdown_sections(self):
        evil = 'x`\n# FORGED\n<script>'
        report = {'baseline_id': evil, 'candidate_id': 'b', 'overall': {'baseline': 1, 'candidate': 0, 'delta': -1}, 'gate': {'passed': False, 'failures': [{'slice': evil, 'reason': 'regressed'}]}, 'cases': [{'case_id': evil, 'delta': -1}]}
        text = markdown(report)
        self.assertTrue('\n# FORGED' not in text)
        self.assertTrue('<script>' not in text)
        self.assertTrue('**BLOCKED**' in text)
