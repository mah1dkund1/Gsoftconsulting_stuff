class BankError(Exception):
    """Base class for all bank relatied errors"""
    
    pass

class InsufficientFundsError(BankError):
    
    def __init__(self, requested, available):
        self.requested = requested
        self.available = available
        
        super().__init__(f"Insufficient funds: Requested {requested}, but only have {available}")
        

class InvalidAmountError(BankError):
    pass

class AccountFrozenError(BankError):
    pass

