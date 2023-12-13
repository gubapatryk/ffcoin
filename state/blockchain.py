from constants import VOID_HASH_PTR, GENESIS_BLOCK_TIMESTAMP
from util.exception.balnce_insufficient_funds_exception import BalanceInsufficientFundsException
from util.exception.blockchain_append_exception import BlockchainAppendException
from util.exception.improper_transfer_exception import ImproperTransferException
from . import Balance
from .block import Block
from .genesis_transaction import GenesisTransaction


class Blockchain:
  def __init__(self):
    self.chain = [self.create_genesis_block()]

  def create_genesis_block(self):
    return Block(GenesisTransaction(), VOID_HASH_PTR, t=GENESIS_BLOCK_TIMESTAMP)

  def add_block_with_data(self, data):
    new_block = Block(data, self.chain[-1].hash)

    # Difficulty level of 4
    new_block.mine_block()
    self.chain.append(new_block)

  def try_append(self, block: Block):
    self.try_can_block_be_added_to_blockchain(block)
    if not block.previous_hash == self.chain[-1].calculate_hash():
      raise BlockchainAppendException("Attempted to add block with improper prev hash")
    if not block.is_nonce_correct():
      raise BlockchainAppendException("Attempted to add block with improper nonce")
    self.chain.append(block)

  def try_can_block_be_added_to_blockchain(self, block: Block) -> None:
    try:
      hypothetical_balance = Balance(self)
      hypothetical_balance.upsert_block(block)
    except BalanceInsufficientFundsException as e:
      balance = Balance(self)  # yes this is reretardere
      raise ImproperTransferException(balance, block) from e

  def display_blocks(self):
    print("-" * 30)
    for block in self.chain:
        print(block.to_dict())
        print("-" * 30)

  def print_filtered(self):
    print("-" * 30)
    for block in self.chain:
        print(block.mined_by)
        print("-" * 30)
