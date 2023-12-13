class BalanceInsufficientFundsException(Exception):
  def __init__(self, user, amount: float):
    self.msg = f"User {user.name} has insufficient funds for operation of {amount}. Blockchain is incorrect"
    super().__init__(self.msg)
