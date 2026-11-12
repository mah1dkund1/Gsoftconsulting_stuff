from bank.bank.accounts import BankAccount
from bank.bank.savings import SavingsAccount
from bank.bank.exceptions import InsufficientFundsError

def run_bank():
    print("--- PART 1 & 4: Account Creation & Dunder Method ---")
    acc1 = BankAccount("", "ACC-001", 100)
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
    
    # Transfer $200 from the savings account to the standard account
    transfer_money(sender=savings, receiver=acc1, amount=200)
    
if __name__ == "__main__":
    run_bank()