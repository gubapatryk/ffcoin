from state import User


class BalanceInsufficientFundsException(Exception):
  def __init__(self, user: User, amount: float):
    self.msg = f"User {user.name} has insufficient funds for operation of {amount}. Blockchain is incorrect"
    super().__init__(self.msg)
