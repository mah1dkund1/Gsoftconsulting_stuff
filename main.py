from bank.bank.accounts import BankAccount
from bank.bank.savings import SavingsAccount
from bank.bank.exceptions import InsufficientFundsError

def run_bank():
    print("--- PART 1 & 4: Account Creation & Dunder Method ---")
    acc1 = BankAccount("Mahid Kundi", "ACC-001", 100)
    print(acc1) 

    print("\n--- PART 2: Encapsulation & Exceptions ---")
    acc1.deposit(50)
    try:
        acc1.withdraw(500) 
    except InsufficientFundsError as e:
        print(f"Successfully caught the custom error: {e}")

    print("\n--- PART 3: Inheritance (Savings Account) ---")
    savings = SavingsAccount("Mahid Savings", "ACC-002", interest_rate=0.05, _balance=1000)
    print(savings)
    
    print("Adding interest...")
    savings.add_interest() 
    print(savings) # Balance should now be 1050

    print("\n--- PART 5: Protocols & Transfers ---")
    from bank.bank.transactions import transfer_money
    
    transfer_money(sender=savings, receiver=acc1, amount=200)
 
 
 
    
        
    print("\n--- PART 4: Abstraction & Polymorphism ---")
    from bank.bank.transactions import DepositTransaction, WithdrawTransaction, TransferTransaction, run_all
    from bank.bank.protocols import EmailNotifier, SMSNotifier, process
        
    poly_acc1 = BankAccount("Mahid", "POLY-1", 100)
    poly_acc2 = BankAccount("Ali", "POLY-2", 0)

    my_transactions = [
            DepositTransaction(500),            
            WithdrawTransaction(200),           
            TransferTransaction(150, poly_acc2)  
        ]

    print(f"Starting balance: {poly_acc1.balance}")
        
    run_all(my_transactions, poly_acc1)
        
    print(f"Ending balance Mahid: {poly_acc1.balance}")
    print(f"Ending balance Ali: {poly_acc2.balance}")  

    print("\nTesting Notifiers:")
    email_service = EmailNotifier()
    sms_service = SMSNotifier()
        
    process(DepositTransaction(50), poly_acc1, email_service)
    process(WithdrawTransaction(20), poly_acc1, sms_service)



if __name__ == "__main__":
    run_bank()