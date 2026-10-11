from .storage import load_tickets, save_tickets
from .tickets import create_ticket as add_ticket


class TicketManager:

    tickets_file_name = "tickets_logs.json"

    def __init__(self):
        self.tickets_file_name = self.__class__.tickets_file_name
        message, self.tickets = load_tickets(self.tickets_file_name)
        if message:
            print(message)

    def run_menu(self):
        while True:
            print("""
====================================
        CAMPUSFLOW HELPDESK         
====================================
1. Create Ticket
2. List All Tickets
3. View Ticket Details
4. Assign Ticket
5. Update Ticket Status
6. View Work Queue
7. Generate Reports
8. Exit
====================================
""")
            users_choice = get_users_choice()

            if users_choice == 8:
                print("Exiting...")
                break
            if users_choice == 1:
                try:
                    self.create_ticket_from_input()
                except ValueError as error:
                    print(f"Error: {error}")
            elif users_choice in range(2, 8):
                print("This option is not available yet.")
            else:
                print("Choose a valid input.")

    def create_ticket_from_input(self):
        title = input("Enter ticket title: ")
        category = self._get_choice(
            "----->Select category<-----", ["Network", "Hardware", "Software", "Other"]
        )
        urgency = self._get_choice(
            "----->Select urgency<-----", ["low", "medium", "high"]
        )
        try:
            affected_users = int(input("Enter number of affected users: "))
        except ValueError:
            print("Affected users must be a positive integer.")
            return

        ticket = add_ticket(
            self.tickets, title, category, urgency, affected_users
        )
        print(f"Created ticket {ticket['id']}.")
        self._save_tickets()

    def _get_choice(self, prompt, options):
        print(f"\n----->{prompt}<-----")
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")

        choice = input("Enter choice: ").strip()
        try:
            choice_index = int(choice)
            if choice_index < 1 or choice_index > len(options):
                raise ValueError
            return options[choice_index - 1]
        except ValueError:
            raise ValueError("Select a valid choice") from None

    def _save_tickets(self):
        print(save_tickets(self.tickets_file_name, self.tickets))


def get_users_choice() -> int:
    users_choice = input("Enter your choice: ")

    try:
        return int(users_choice)
    except ValueError:
        return 0
   