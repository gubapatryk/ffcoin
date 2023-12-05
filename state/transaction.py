from constants import JSON_CONSTANTS
from state import User
from state.user import user_from_dict_with_opt_key


class Transaction:
  def __init__(self, from_user: User, to_user: User, amount: float, award: float):
    self.from_user = from_user
    self.to_user = to_user
    self.amount = amount
    self.award = award

  def __eq__(self, other):
    if isinstance(other, Transaction):
      return self.from_user == other.from_user and self.to_user == other.to_user and self.amount == other.amount
    return False

  def to_dict(self) -> dict:
    return {
      JSON_CONSTANTS["FROM_USER_KEY"]: self.from_user.to_dict(),
      JSON_CONSTANTS["TO_USER_KEY"]: self.to_user.to_dict(),
      JSON_CONSTANTS["TRANSACTION_AMOUNT_KEY"]: self.amount,
      JSON_CONSTANTS["TRANSACTION_AWARD_KEY"]: self.award,
    }


def transaction_from_dict(d: dict) -> Transaction:
  return Transaction(
    user_from_dict_with_opt_key(d[JSON_CONSTANTS["FROM_USER_KEY"]]),
    user_from_dict_with_opt_key(d[JSON_CONSTANTS["TO_USER_KEY"]]),
    d[JSON_CONSTANTS["TRANSACTION_AMOUNT_KEY"]],
    d[JSON_CONSTANTS["TRANSACTION_AWARD_KEY"]]
  )
