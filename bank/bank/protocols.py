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
        
class Notifier(Protocol):
    def notify(self, message: str) -> None:
        ...

class EmailNotifier:
    def notify(self, message: str) -> None:
        print(f"[EMAIL SENDING] {message}")

class SMSNotifier:
    def notify(self, message: str) -> None:
        print(f"[SMS SENDING] {message}")

def process(transaction, account, notifier: Notifier):
    transaction.apply(account)
    notifier.notify(f"Successfully processed: {transaction.description}")