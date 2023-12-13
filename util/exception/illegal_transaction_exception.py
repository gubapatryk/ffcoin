class IllegalTransactionException(Exception):
  def __init__(self, amount: float):
    self.msg = f"Attempted to create a transaction with amount {amount}"
    super().__init__(self.msg)
