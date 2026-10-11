class TicketWorkflow:
    def __init__(self, tickets_collection):
        self.tickets_collection = tickets_collection

    def _find_ticket(self, ticket_id):
        ticket = self.tickets_collection.get(ticket_id)

        if ticket is None:
            raise KeyError(f"Ticket '{ticket_id}' was not found.")

        return ticket

    def assign_ticket(self, ticket_id, mentor_name):
        """Assign a ticket to a staff member and return the updated ticket."""
        ticket = self._find_ticket(ticket_id)

        if ticket.get("status") == "resolved":
            raise ValueError(
                "A resolved ticket must be reopened before it can be changed."
            )

        if not isinstance(mentor_name, str) or not mentor_name.strip():
            raise ValueError("Mentor name cannot be empty.")

        # Store the name without accidental spaces around it.
        ticket["assigned_to"] = mentor_name.strip()
        return ticket

    def update_status(self, ticket_id, new_status):
        ticket = self._find_ticket(ticket_id)

        if not isinstance(new_status, str):
            raise ValueError("Status must be text.")

        new_status = new_status.strip().lower()
        current_status = ticket.get("status")

        allowed_statuses = {"open", "in_progress", "resolved"}
        if new_status not in allowed_statuses:
            raise ValueError(
                "Invalid status. Use 'open', 'in_progress', or 'resolved'."
            )

        # Reopening is the only allowed change from resolved.
        if current_status == "resolved":
            if new_status == "open":
                ticket["status"] = "open"
                return ticket

            raise ValueError(
                "A resolved ticket must be reopened to 'open' first."
            )

        # Do not accept a request that makes no change.
        if new_status == current_status:
            raise ValueError(f"Ticket is already '{current_status}'.")

        if current_status == "open" and new_status == "in_progress":
            assigned_to = ticket.get("assigned_to")
            if not isinstance(assigned_to, str) or not assigned_to.strip():
                raise ValueError(
                    "Assign the ticket to a staff member before starting work."
                )

            ticket["status"] = "in_progress"
            return ticket

        if current_status == "in_progress" and new_status == "resolved":
            ticket["status"] = "resolved"
            return ticket

        raise ValueError(
            f"Cannot change status from '{current_status}' to '{new_status}'."
        )

    def get_work_queue(self):
        """Return open tickets ordered by priority, then numeric ticket ID."""
        priority_order = {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3,
        }

        open_tickets = []
        for ticket in self.tickets_collection.values():
            if ticket.get("status") == "open":
                open_tickets.append(ticket)

        def sort_key(ticket):
            priority = str(ticket.get("priority", "low")).lower()
            ticket_id = str(ticket.get("id", ""))

            # T012 becomes 12. A nonstandard ID is placed after normal IDs.
            number_part = ticket_id[1:] if ticket_id.startswith("T") else ""
            if number_part.isdigit():
                numeric_id = int(number_part)
            else:
                numeric_id = float("inf")

            return (priority_order.get(priority, 4), numeric_id)

        return sorted(open_tickets, key=sort_key)