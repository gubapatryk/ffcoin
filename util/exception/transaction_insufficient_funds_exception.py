from state import User, BalanceEntry


class TransactionInsufficientFundsException(Exception):
  def __init__(self, balance: BalanceEntry, amount: float):
    self.msg = f"Insufficient funds for operation of {amount}. User has {balance.balance}"
    super().__init__(self.msg)
