from bank.bank.accounts import BankAccount

class SavingsAccount(BankAccount):
    
    def __init__(self, owner, account_id, interest_rate, _balance=0):
        
        super().__init__(owner, account_id, _balance)
        
        self.interest_rate = interest_rate
        
        
    def add_interest(self):
        
        interest_amount = self.balance*self.interest_rate
        self.deposit(interest_amount)
