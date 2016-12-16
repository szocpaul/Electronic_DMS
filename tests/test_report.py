import unittest

from reports import Report
from repository import Repository


class TestReport(unittest.TestCase):
    """Test the report class"""

    def test_report_creation(self):
        report = Report()

    def test_report_properties(self):
        role_counts = {
            'admin': 1,
            'manager': 3,
            'author': 5,
            'reviewer': 6,
            'visitor': 3
        }
        report = Report(user_count=10, document_count=3, user_count_by_roles=role_counts, import_count=0, export_count=4)
        self.assertEqual(report.user_count, 10)
        self.assertEqual(report.document_count, 3)
        self.assertEqual(report.user_count_by_roles, role_counts)
        self.assertEqual(report.import_count, 0)
        self.assertEqual(report.export_count, 4)

    def test_get_report_from_empty_repository(self):
        role_counts = {
            'admin': 0,
            'manager': 0,
            'author': 0,
            'reviewer': 0,
            'visitor': 0
        }
        repository = Repository('Empty', '/tmp/test_repo')
        report = repository.create_report()
        self.assertEqual(report.user_count, 0)
        self.assertEqual(report.document_count, 0)
        self.assertEqual(report.user_count_by_roles, role_counts)
        self.assertEqual(report.import_count, 0)
        self.assertEqual(report.export_count, 0)
