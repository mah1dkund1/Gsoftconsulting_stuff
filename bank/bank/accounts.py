class BankAccounts:
    
    total_accounts = 0
    
    def __init__(self , owner , account_id , _balance = 0):
        
        self.owner = owner
        self.account_id = account_id
        self._balance = _balance
        
        BankAccounts.total_accounts+=1
        

 # for depositing money

        
    def deposit (self , deposit_amount):
        
        if not self.is_valid_amount(deposit_amount):
            print("Error: Invalid Deposit Amount")
            return 
        
        self._balance = self._balance + deposit_amount
        
        print(f"Successfully added {deposit_amount}. New balance: {self._balance}") 
    
  
  # withdrawing money
  
    def withdraw (self , withdraw_amount ):
        
       if not self.is_valid_amount(withdraw_amount):
           print (f"Invalid Withdraw amount ")
           return 
       
        
       if self._balance - withdraw_amount < 0:
            print("Erorr : insufficient funds.")
            return
        
       self._balance -= withdraw_amount
        
       print(f"Successfully withdrew {withdraw_amount}. New balance: {self._balance}") 
        
   
   
   
   
   
    @staticmethod
    def is_valid_amount(amount):
        return amount > 0
    
    @classmethod
    def from_dict(cls, data):
        
        owner_name = data["owner"]
        
        temp_id = "ACC-999"
        
        new_account = cls(owner_name, temp_id, data["balance"])
        
        
        return new_account