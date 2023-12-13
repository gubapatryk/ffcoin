from state import Balance
from state.block import Block


class ImproperTransferException(Exception):
  def __init__(self, balance: Balance, block: Block):
    self.msg = f"Block can't be accepted to blockchain\n{block.to_dict()}\n{balance}"
    super().__init__(self.msg)
