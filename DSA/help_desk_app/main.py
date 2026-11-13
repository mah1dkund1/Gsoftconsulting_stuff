from system import HelpDesk

def main():
    
    desk = HelpDesk()
    
    ticket_counter = 1
    
    
    while True:
        print("\n--- Help Desk System ---")
        print("1. Raise Ticket")
        print("2. Resolve Ticket")
        print("3. Undo Last Resolution")
        print("4. View Queue State (Head)")
        print("5. Exit") 
        
        choice = input("Select an option: ")
        
        if choice == '1':
            name = input("Customer Name: ")
            issue = input("Issue Description: ")
            desk.raise_ticket(ticket_counter, name, issue)
            
            print(f"Ticket #{ticket_counter} raised for {name}.")
            ticket_counter +=1
            
        
        elif choice == '2':
            resolved = desk.resolve_ticket()
            if resolved:
                print(f"Resolved Ticket: {resolved}")
                
            else: 
                print("Queue is empty.")
                
        elif choice == '3':
            undone = desk.undo_action()
            if undone:
                print(f"Undid resolution for Ticket: {undone}")
            else:
                print("Nothing to undo.")
            
        elif choice =='4':
            if desk.head:
                print(f"Next up: {desk.head.data}")
            else:
                print("Queue is currently empty.")
                
        elif choice == '5':
            print("Exiting system. Goodbye!")
            break
        
        else:
            print("Invalid Selection")
            
if __name__ == "__main__":
    main()
                
                
            
            
        
        