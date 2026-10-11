tickets_collection = {
    "T001": {
        "id": "T001",
        "title": "Wi-Fi is not working",
        "assigned_to": None,
        "status": "open"
    },
    "T002": {
        "id": "T002",
        "title": "Laptop won't start",
        "assigned_to": "Sam",
        "status": "in_progress"
    }
}

def find_ticket(tickets_collection, id ):
        tickets = tickets_collection.get(id)
        if tickets is None:
            return "ticket not found"
        else:
              return tickets
        
def change_tickets(tickets_collection, id):
      tickets = tickets_collection.get(id)
      if tickets is None:
            return "ticket not found"
      if tickets["assigned_to"] == None:
            tickets["assigned_to"] = "Ada"
            return "tickets changed succesfully"
      else:
            return tickets["assigned_to"]
                                    
def assign_ticket(tickets_collection, ticket_id, mentor_name):
    tickets = tickets_collection.get(ticket_id)
    if tickets == None:
          return "tickets not found"
    if mentor_name == "" or mentor_name.strip() == False:
          return "invalid mentor name"
                
    if tickets["assigned_to"] == None:
          tickets["assigned_to"] = mentor_name
          return "Ticket assigned successfully"
    else:
          return {tickets["assigned_to"]}
    # Your implementation goes here.
    pass


print(find_ticket(tickets_collection, "T001"))
print(change_tickets(tickets_collection, "T002"))