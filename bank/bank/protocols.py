from typing import Protocol

class AccountProtocol(Protocol):
    """Defines the blueprint that any account must follow."""
    
    @property
    def balance(self) -> float:
        ...
        
    def deposit(self, amount: float) -> None:
        ...
        
    def withdraw(self, amount: float) -> None:
        ...