import unittest

from campusflow.tickets import calculate_priority, create_ticket


class TestTicketCreation(unittest.TestCase):
    def test_priority_rules(self):
        self.assertEqual(calculate_priority("high", 10), "critical")
        self.assertEqual(calculate_priority("high", 1), "high")
        self.assertEqual(calculate_priority("low", 10), "high")
        self.assertEqual(calculate_priority("medium", 1), "medium")
        self.assertEqual(calculate_priority("low", 3), "medium")
        self.assertEqual(calculate_priority("low", 2), "low")

    def test_priority_accepts_urgency_case_variations(self):
        self.assertEqual(calculate_priority(" HIGH ", 10), "critical")

    def test_create_ticket_saves_all_fields(self):
        tickets = {}

        ticket = create_ticket(
            tickets, " Wi-Fi is down ", "network", "HIGH", 12
        )

        self.assertEqual(ticket, {
            "id": "T001",
            "title": "Wi-Fi is down",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
        })
        self.assertEqual(tickets["001"], ticket)

    def test_ticket_ids_continue_from_existing_tickets(self):
        tickets = {
            "T001": {"id": "T001"},
            "T003": {"id": "T003"},
        }

        ticket = create_ticket(tickets, "Broken laptop", "Hardware", "low", 1)

        self.assertEqual(ticket["id"], "T004")
        self.assertEqual(tickets["004"], ticket)

    def test_ticket_ids_continue_from_numeric_ticket_keys(self):
        tickets = {
            "001": {"id": "T001"},
            "003": {"id": "T003"},
        }

        ticket = create_ticket(tickets, "Broken laptop", "Hardware", "low", 1)

        self.assertEqual(ticket["id"], "T004")
        self.assertEqual(tickets["004"], ticket)

    def test_create_ticket_rejects_blank_title(self):
        with self.assertRaisesRegex(ValueError, "Title must not be blank"):
            create_ticket({}, "  ", "Network", "low", 1)

    def test_create_ticket_rejects_invalid_category(self):
        with self.assertRaisesRegex(ValueError, "Category must be"):
            create_ticket({}, "Cannot connect", "Invalid", "low", 1)

    def test_create_ticket_rejects_invalid_urgency(self):
        with self.assertRaisesRegex(ValueError, "Urgency must be"):
            create_ticket({}, "Cannot connect", "Network", "urgent", 1)

    def test_create_ticket_rejects_invalid_affected_users(self):
        for value in [0, -1, 1.5, "3", True]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "positive integer"):
                    create_ticket({}, "Cannot connect", "Network", "low", value)

    def test_invalid_ticket_does_not_change_ticket_collection(self):
        tickets = {}

        with self.assertRaises(ValueError):
            create_ticket(tickets, "", "Network", "low", 1)

        self.assertEqual(tickets, {})


if __name__ == "__main__":
    unittest.main()