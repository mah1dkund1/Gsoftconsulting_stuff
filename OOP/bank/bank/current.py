from bank.bank.accounts import BankAccount
from bank.bank.exceptions import InsufficientFundsError, InvalidAmountError, AccountFrozenError


class CurrentAccount(BankAccount):

    def __init__(self, owner, account_id, overdraft_limit=500, _balance=0):

        super().__init__(owner, account_id, _balance)

        self.overdraft_limit = overdraft_limit


    # current account can go below zero, up to the overdraft limit
    def withdraw(self, withdraw_amount):

        if self.frozen:
            raise AccountFrozenError("Account is frozen!")

        if not self.is_valid_amount(withdraw_amount):
            raise InvalidAmountError("Amount must be positive")

        if self._balance - withdraw_amount < -self.overdraft_limit:
            raise InsufficientFundsError(withdraw_amount, self._balance + self.overdraft_limit)

        self._balance -= withdraw_amount

        print(f"Successfully withdrew {withdraw_amount}. New balance: {self._balance}")


    def is_overdrawn(self):
        return self._balance < 0


    def __str__(self):
        return f"Current Account {self.account_id} ({self.owner}): Balance ${self.balance} | Overdraft limit ${self.overdraft_limit}"
