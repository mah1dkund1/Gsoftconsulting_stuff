from abc import ABC, abstractmethod
from bank.bank.protocols import AccountProtocol

def transfer_money(sender: AccountProtocol, receiver: AccountProtocol, amount: float):
    """Transfers money between any two objects that match the AccountProtocol."""
    
    sender.withdraw(amount)
    receiver.deposit(amount)
    
    print(f"Transfer complete. Sender balance: {sender.balance} | Receiver balance: {receiver.balance}")