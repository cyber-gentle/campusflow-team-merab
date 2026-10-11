import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from campusflow.workflow import TicketManager


class TestTicketManagerWorkflow(unittest.TestCase):
    @patch("campusflow.workflow.save_tickets")
    @patch("campusflow.workflow.load_tickets", return_value=("", {}))
    def test_menu_creates_ticket_and_persists_changes(
        self, load_tickets, save_tickets
    ):
        output = io.StringIO()
        choices = ["1", "Wi-Fi outage", "1", "3", "12", "8"]

        with patch("builtins.input", side_effect=choices), redirect_stdout(output):
            TicketManager().run_menu()

        load_tickets.assert_called_once_with("tickets_logs.json")
        saved_tickets = save_tickets.call_args.args[1]
        self.assertEqual(saved_tickets["001"]["title"], "Wi-Fi outage")
        self.assertEqual(saved_tickets["001"]["priority"], "critical")
        self.assertIn("Created ticket T001.", output.getvalue())
        self.assertIn("2. List All Tickets", output.getvalue())
        self.assertIn("8. Exit", output.getvalue())

    @patch("campusflow.workflow.load_tickets", return_value=("", {}))
    def test_get_choice_returns_selected_option(self, load_tickets):
        manager = TicketManager()

        with patch("builtins.input", return_value="2"):
            self.assertEqual(manager._get_choice("Select category", ["A", "B"]), "B")
        load_tickets.assert_called_once_with("tickets_logs.json")

    @patch("campusflow.workflow.load_tickets", return_value=("", {}))
    def test_get_choice_rejects_out_of_range_selection(self, load_tickets):
        manager = TicketManager()

        with patch("builtins.input", return_value="3"):
            with self.assertRaisesRegex(ValueError, "Select a valid choice"):
                manager._get_choice("Select category", ["A", "B"])
        load_tickets.assert_called_once_with("tickets_logs.json")

    @patch("campusflow.workflow.load_tickets", return_value=("", {}))
    def test_menu_reports_invalid_choices_and_exits(self, load_tickets):
        output = io.StringIO()

        with patch("builtins.input", side_effect=["not a number", "9", "8"]), \
                redirect_stdout(output):
            TicketManager().run_menu()

        self.assertEqual(output.getvalue().count("Choose a valid input."), 2)
        self.assertIn("Exiting...", output.getvalue())
        load_tickets.assert_called_once_with("tickets_logs.json")

    @patch(
        "campusflow.workflow.load_tickets",
        return_value=("", {"T007": {"id": "T007", "status": "open"}}),
    )
    def test_manager_loads_ticket_dictionary_from_storage_tuple(self, load_tickets):
        manager = TicketManager()

        self.assertEqual(manager.tickets, {"T007": {"id": "T007", "status": "open"}})
        load_tickets.assert_called_once_with("tickets_logs.json")


if __name__ == "__main__":
    unittest.main()