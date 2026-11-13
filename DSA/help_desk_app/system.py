class Node:
    
    def __init__(self, ticket_record):
        self.data = ticket_record
        self.next = None
        
        
class HelpDesk:
    
    def __init__(self):
        
        self.head = None
        self.tail = None
        self.ticket_lookup = {}
        
        
        
        self.unique_customers = set()
        
        self.resolved_history = []
        
        self.undo_stack = []
        
    
    def raise_ticket(self, ticket_id, customer_name, issue):
        
        #tuple for customer data
        ticket_record = (ticket_id, customer_name, issue)
        
        self.unique_customers.add(customer_name)
        self.ticket_lookup[ticket_id] = ticket_record
        
        new_node = Node(ticket_record)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        
        else:
            self.tail.next = new_node
            self.tail = new_node
        
    
    def resolve_ticket(self):
        
        if self.head is None:
            return None
        
        resolved_record = self.head.data
        self.head = self.head.next
        
        if self.head is None:
            self.tail = None
            
        self.resolved_history.append(resolved_record)
        
        self.undo_stack.append(resolved_record)
        
        self.undo_stack.append(resolved_record)
        
        return resolved_record
        
    def undo_action(self):
        
        if not self.undo_stack:
            return None
        
        #pop latest resovled from stack and remove from resolved tickets list
        record = self.undo_stack.pop()
        
        
        if record in self.resolved_history:
            self.resolved_history.remove(record)
            
        new_node = Node(record)
        new_node.next = self.head
        self.head = new_node
        
        if self.tail is None:
            self.tail = new_node
            
        return record
    
        
        
            
            