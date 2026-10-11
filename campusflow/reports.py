"""Reporting helpers for CampusFlow."""


class TicketReports:
    """Create a summary of the current ticket collection."""

    def __init__(self, tickets_collection):
        self.tickets_collection = tickets_collection

    def generate_report(self):
        """Return total tickets and complete status/priority breakdowns."""
        statuses = {
            "open": 0,
            "in_progress": 0,
            "resolved": 0,
        }
        priorities = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }

        for ticket in self.tickets_collection.values():
            status = str(ticket.get("status", "")).lower()
            priority = str(ticket.get("priority", "")).lower()

            if status in statuses:
                statuses[status] += 1

            if priority in priorities:
                priorities[priority] += 1

        return {
            "total_tickets": len(self.tickets_collection),
            "by_status": statuses,
            "by_priority": priorities,
        }

    def format_report(self):
        """Return a simple, readable text report for the CLI."""
        report = self.generate_report()
        lines = [
            "CampusFlow Ticket Report",
            "------------------------",
            f"Total tickets: {report['total_tickets']}",
            "",
            "By status:",
        ]

        for status, count in report["by_status"].items():
            lines.append(f"  {status}: {count}")

        lines.append("")
        lines.append("By priority:")

        for priority, count in report["by_priority"].items():
            lines.append(f"  {priority}: {count}")

        return "\n".join(lines)