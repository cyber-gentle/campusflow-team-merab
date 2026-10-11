import unittest

from campusflow.workflow import TicketWorkflow


def sample_tickets():
    return {
        "T001": {
            "id": "T001",
            "title": "Wi-Fi is not working",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
        },
        "T002": {
            "id": "T002",
            "title": "Laptop will not start",
            "category": "Hardware",
            "urgency": "medium",
            "affected_users": 2,
            "priority": "medium",
            "status": "open",
            "assigned_to": "Sam",
        },
        "T003": {
            "id": "T003",
            "title": "Old resolved issue",
            "category": "Software",
            "urgency": "low",
            "affected_users": 1,
            "priority": "low",
            "status": "resolved",
            "assigned_to": "Ada",
        },
    }


class TestTicketAssignment(unittest.TestCase):
    def setUp(self):
        self.tickets = sample_tickets()
        self.workflow = TicketWorkflow(self.tickets)

    def test_assign_ticket_updates_dictionary(self):
        ticket = self.workflow.assign_ticket("T001", "Ada")
        self.assertEqual(ticket["assigned_to"], "Ada")
        self.assertEqual(self.tickets["T001"]["assigned_to"], "Ada")

    def test_assignment_trims_name_spaces(self):
        ticket = self.workflow.assign_ticket("T001", "  Ada  ")
        self.assertEqual(ticket["assigned_to"], "Ada")

    def test_unknown_ticket_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.workflow.assign_ticket("T999", "Ada")

    def test_empty_mentor_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.workflow.assign_ticket("T001", "")

    def test_spaces_only_mentor_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.workflow.assign_ticket("T001", "   ")

    def test_resolved_ticket_must_be_reopened_before_assignment(self):
        with self.assertRaises(ValueError):
            self.workflow.assign_ticket("T003", "Sam")


class TestTicketStatus(unittest.TestCase):
    def setUp(self):
        self.tickets = sample_tickets()
        self.workflow = TicketWorkflow(self.tickets)

    def test_unassigned_ticket_cannot_start_work(self):
        with self.assertRaises(ValueError):
            self.workflow.update_status("T001", "in_progress")
        self.assertEqual(self.tickets["T001"]["status"], "open")

    def test_assigned_ticket_can_move_to_in_progress(self):
        ticket = self.workflow.update_status("T002", "in_progress")
        self.assertEqual(ticket["status"], "in_progress")

    def test_in_progress_ticket_can_be_resolved(self):
        self.workflow.update_status("T002", "in_progress")
        ticket = self.workflow.update_status("T002", "resolved")
        self.assertEqual(ticket["status"], "resolved")

    def test_resolved_ticket_can_be_reopened(self):
        ticket = self.workflow.update_status("T003", "open")
        self.assertEqual(ticket["status"], "open")

    def test_resolved_ticket_cannot_skip_reopening(self):
        with self.assertRaises(ValueError):
            self.workflow.update_status("T003", "in_progress")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            self.workflow.update_status("T002", "working")

    def test_unknown_ticket_status_update_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.workflow.update_status("T999", "open")


class TestWorkQueue(unittest.TestCase):
    def setUp(self):
        self.tickets = sample_tickets()
        self.tickets["T004"] = {
            "id": "T004", "title": "Small issue", "category": "Other",
            "urgency": "low", "affected_users": 1, "priority": "low",
            "status": "open", "assigned_to": None
        }
        self.tickets["T005"] = {
            "id": "T005", "title": "Another high issue", "category": "Network",
            "urgency": "high", "affected_users": 2, "priority": "high",
            "status": "open", "assigned_to": None
        }
        self.workflow = TicketWorkflow(self.tickets)

    def test_queue_sorts_by_priority_then_numeric_id(self):
        queue_ids = [ticket["id"] for ticket in self.workflow.get_work_queue()]
        self.assertEqual(queue_ids, ["T001", "T005", "T002", "T004"])

    def test_queue_excludes_resolved_tickets(self):
        queue_ids = [ticket["id"] for ticket in self.workflow.get_work_queue()]
        self.assertNotIn("T003", queue_ids)

    def test_empty_queue_returns_empty_list(self):
        workflow = TicketWorkflow({})
        self.assertEqual(workflow.get_work_queue(), [])


if __name__ == "__main__":
    unittest.main()