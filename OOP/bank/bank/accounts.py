from bank.bank.exceptions import BankError, InsufficientFundsError, InvalidAmountError, AccountFrozenError





class BankAccount:
    
    total_accounts = 0
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, new_owner):
        if not new_owner or not isinstance(new_owner, str):
            raise ValueError("Owner Name cannot be an empty string.")
        
        self._owner = new_owner
    
    
    def __init__(self , owner , account_id , _balance = 0):
        
        self.frozen = False
        self.owner = owner
        self.account_id = account_id
        self._balance = _balance
        
        BankAccount.total_accounts+=1
        

 # for depositing money

        
    def deposit (self , deposit_amount):
        
        if self.frozen:
            raise AccountFrozenError("Account is frozen!")
        
        if not self.is_valid_amount(deposit_amount):
            print("Error: Invalid Deposit Amount")
            return 
        
        self._balance = self._balance + deposit_amount
        
        print(f"Successfully added {deposit_amount}. New balance: {self._balance}") 
    
  
  # withdrawing money
  
    def withdraw (self , withdraw_amount ):
        
       if self.frozen:
           raise AccountFrozenError("Account if frozen error")
       
       if not self.is_valid_amount(withdraw_amount):
           raise InvalidAmountError("Amount must be positive")
            
       
        
       if self._balance - withdraw_amount < 0:
            raise InsufficientFundsError(withdraw_amount, self._balance)
            
        
       self._balance -= withdraw_amount
        
       print(f"Successfully withdrew {withdraw_amount}. New balance: {self._balance}") 
        
   
    def __str__(self):
        
        return f"Account {self.account_id} ({self.owner}): Balance ${self.balance}"
   
   
   
   
    @staticmethod
    def is_valid_amount(amount):
        return amount > 0
    
    @classmethod
    def from_dict(cls, data):
        
        owner_name = data["owner"]
        
        temp_id = "ACC-999"
        
        new_account = cls(owner_name, temp_id, data["balance"])
        
        
        return new_account