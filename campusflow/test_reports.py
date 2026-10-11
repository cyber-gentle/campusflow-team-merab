import unittest

from campusflow.reports import TicketReports


class TestTicketReports(unittest.TestCase):
    def test_empty_collection_report(self):
        report = TicketReports({}).generate_report()
        self.assertEqual(report["total_tickets"], 0)
        self.assertEqual(report["by_status"]["open"], 0)
        self.assertEqual(report["by_priority"]["critical"], 0)

    def test_report_counts_status_and_priority(self):
        tickets = {
            "T001": {"status": "open", "priority": "critical"},
            "T002": {"status": "in_progress", "priority": "medium"},
            "T003": {"status": "resolved", "priority": "low"},
            "T004": {"status": "open", "priority": "high"},
        }

        report = TicketReports(tickets).generate_report()

        self.assertEqual(report["total_tickets"], 4)
        self.assertEqual(report["by_status"]["open"], 2)
        self.assertEqual(report["by_status"]["in_progress"], 1)
        self.assertEqual(report["by_status"]["resolved"], 1)
        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["high"], 1)
        self.assertEqual(report["by_priority"]["medium"], 1)
        self.assertEqual(report["by_priority"]["low"], 1)

    def test_format_report_returns_readable_text(self):
        report_text = TicketReports({}).format_report()
        self.assertIn("Total tickets: 0", report_text)
        self.assertIn("By status:", report_text)
        self.assertIn("By priority:", report_text)


if __name__ == "__main__":
    unittest.main()