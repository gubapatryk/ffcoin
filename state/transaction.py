from constants import JSON_CONSTANTS
from state import User


class Transaction:
  def __init__(self, from_user: User, to_user: User, amount: float, award: float):
    self.from_user = from_user
    self.to_user = to_user
    self.amount = amount
    self.award = award

  def to_dict(self) -> dict:
    return {
      JSON_CONSTANTS["FROM_USER_KEY"]: self.from_user.to_dict(),
      JSON_CONSTANTS["TO_USER_KEY"]: self.to_user.to_dict(),
      JSON_CONSTANTS["TRANSACTION_AMOUNT_KEY"]: self.amount,
      JSON_CONSTANTS["TRANSACTION_AWARD_KEY"]: self.award,
    }
