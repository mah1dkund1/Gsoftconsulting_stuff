import pytest
from system import HelpDesk

def test_raise_ticket():
    
    desk = HelpDesk()
    desk.raise_ticket(1, "Alice", "Login issue")
    
    assert desk.head.data == (1, "Alice", "Login issue")
    
    assert desk.head.data == (1, "Alice", "Login issue")
    assert desk.head == desk.tail
    
    
    assert "Alice" in desk.unique_customers
    assert desk.ticket_lookup[1] == (1, "Alice", "Login Issue")
    
def test_resolve_ticket():
    desk = HelpDesk()
    
    
    desk.raise_ticket(1, "Alice", "Login issue")
    
    desk.raise_ticket(2, "Bob", "Crash on startup")    
    
    resolved = desk.resolve_ticket()
    assert resolved == (1, "Alice", "login issue")
    assert desk.head.data == (2,"Bob", "ccrash on startup")
    assert len(desk.resolved_history) == 1
    assert len(desk.undo_stack) == 1
    

def test_undo_action():
    
    desk = HelpDesk()
    desk.raise_ticket(1, "Alice", "Login issue")

    desk.resolve_ticket()
    
    undone = desk.undo_action()
    
    assert undone == (1, "Alice", "Login issue")
    assert desk.head.data == (1,"Alice", "Login issue")
    assert len(desk.resolved_history) == 0
    assert len(desk.undo_stack) == 0