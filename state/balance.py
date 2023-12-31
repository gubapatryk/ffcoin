from constants import INITIAL_BALANCE
from state.block import Block
from util.exception.balnce_insufficient_funds_exception import BalanceInsufficientFundsException


class Balance:

  def __init__(self, blockchain: list[Block]):
    self.balance: dict[str, BalanceEntry] = dict()
    for block in blockchain:
      if not block.is_genesis():
        self.upsert_block(block)

  def __str__(self):
    out = "\n".join(map(lambda entry: f"{entry.user.name}: {entry.balance}", self.balance.values()))
    out = out + f"\nEvery other user has {INITIAL_BALANCE}"
    return out

  def upsert_block(self, block: Block):
    if block.mined_by is None:
      assert (block.data.from_user.ip != block.data.to_user.ip)
    else:
      assert (block.mined_by.ip != block.data.from_user.ip != block.data.to_user.ip)
      self.upsert_balance_entry(block.mined_by, block.data.award)
    self.upsert_balance_entry(block.data.from_user, -block.data.amount)
    self.upsert_balance_entry(block.data.to_user, block.data.amount)

  def upsert_balance_entry(self, user, amount: float) -> dict:
    current_balance: BalanceEntry = self.balance.get(user.ip)
    amount = amount + INITIAL_BALANCE if current_balance is None else current_balance.balance + amount
    if amount < 0.0:
      raise BalanceInsufficientFundsException(user, amount)
    self.balance[user.ip] = BalanceEntry(user, amount)
    return self.balance


class BalanceEntry:

  def __init__(self, user, balance: float):
    self.user = user
    self.balance = balance
