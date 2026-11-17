from abc import ABC, abstractmethod
from bank.bank.protocols import AccountProtocol


class Transaction(ABC):
    """Abstract base class for all transactions."""
    
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def apply(self, account) -> None:
        pass

class DepositTransaction(Transaction):
    def __init__(self, amount: float):
        self.amount = amount

    @property
    def description(self) -> str:
        return f"Deposit of ${self.amount}"

    def apply(self, account) -> None:
        account.deposit(self.amount)

class WithdrawTransaction(Transaction):
    def __init__(self, amount: float):
        self.amount = amount

    @property
    def description(self) -> str:
        return f"Withdrawal of ${self.amount}"

    def apply(self, account) -> None:
        account.withdraw(self.amount)

class TransferTransaction(Transaction):
    def __init__(self, amount: float, to_account):
        self.amount = amount
        self.to_account = to_account

    @property
    def description(self) -> str:
        return f"Transfer of ${self.amount} to Account {self.to_account.account_id}"

    def apply(self, account) -> None:
        account.withdraw(self.amount)
        
        try:
            self.to_account.deposit(self.amount)
        except Exception as e:
            account.deposit(self.amount) 
            raise e 

def run_all(transactions: list[Transaction], account):
    """Executes a list of mixed transactions on a single account."""
    for transaction in transactions:
        transaction.apply(account)
        
        
        
def transfer_money(sender: AccountProtocol, receiver: AccountProtocol, amount: float):
    """Transfers money between any two objects that match the AccountProtocol."""
    
    sender.withdraw(amount)
    receiver.deposit(amount)
    
    print(f"Transfer complete. Sender balance: {sender.balance} | Receiver balance: {receiver.balance}")