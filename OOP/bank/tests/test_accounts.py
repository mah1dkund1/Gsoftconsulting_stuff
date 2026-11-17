import pytest
from bank.bank.accounts import BankAccount
from bank.bank.exceptions import InsufficientFundsError, AccountFrozenError, InvalidAmountError

def test_account_creation():
    acc = BankAccount("Mahid","123",100)
    assert acc.owner == "Mahid"
    
    assert acc.balance == 100

def test_frozen_account_raises_error():
    acc = BankAccount("Mahid", "123", 100)
    acc.frozen = True
    
    # pytest.raises checks that your code successfully crashes with the correct error
    with pytest.raises(AccountFrozenError):
        acc.withdraw(50)