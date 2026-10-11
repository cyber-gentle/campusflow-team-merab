def calculate_priority(urgency, affected_users):
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be low, medium, or high.")
    urgency = urgency.strip().lower()
    if urgency not in ["low", "medium", "high"]:
        raise ValueError("Urgency must be low, medium, or high.")
    if not isinstance(affected_users, int) or isinstance(affected_users, bool):
        raise ValueError("Affected users must be a positive integer.")
    if affected_users < 1:
        raise ValueError("Affected users must be a positive integer.")

    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def create_ticket(tickets, title, category, urgency, affected_users):
    if not isinstance(tickets, dict):
        raise TypeError("Tickets must be stored in a dictionary.")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title must not be blank.")

    categories = ["Network", "Hardware", "Software", "Other"]
    if not isinstance(category, str):
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    category = category.strip().title()
    if category not in categories:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    if not isinstance(urgency, str):
        raise ValueError("Urgency must be low, medium, or high.")
    urgency = urgency.strip().lower()
    priority = calculate_priority(urgency, affected_users)

    highest_id = 0
    for ticket_key, ticket in tickets.items():
        ticket_id = ticket.get("id") if isinstance(ticket, dict) else None
        for existing_id in (ticket_key, ticket_id):
            if isinstance(existing_id, int) and not isinstance(existing_id, bool):
                highest_id = max(highest_id, existing_id)
            elif isinstance(existing_id, str):
                number = (
                    existing_id[1:]
                    if existing_id.startswith("T")
                    else existing_id
                )
                if number.isdigit():
                    highest_id = max(highest_id, int(number))

    new_id_number = highest_id + 1
    new_id = f"T{new_id_number:03d}"

    ticket = {
        "id": new_id,
        "title": title.strip(),
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }
    tickets[new_id[1:]] = ticket
    return ticket
