from constants import JSON_CONSTANTS, INITIAL_BALANCE


class GenesisBlock:
  def __init__(self, amount: float = INITIAL_BALANCE):
    self.amount = amount
    self.comment = f"This is a genesis block. It awards each account ${amount} for debug purposes (just to get the economy going)"

  def __eq__(self, other):
    if isinstance(other, GenesisBlock):
      return self.amount == other.amount
    return False

  def to_dict(self) -> dict:
    return {
      JSON_CONSTANTS["TRANSACTION_AMOUNT_KEY"]: self.amount,
      JSON_CONSTANTS["GENESIS_BLOCK_COMMENT"]: self.comment,
    }
