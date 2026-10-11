class TicketManager():

    @staticmethod
    def menu():
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
            else:
                print("Choose a valid input.")


def get_users_choice() -> int:
    users_choice = input("Enter your choice: ")
    
    try:
        users_choice = int(users_choice)
    except Exception:
        return 0

    return users_choice  
   