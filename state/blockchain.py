from constants import VOID_HASH_PTR
from util.exception.blockchain_append_exception import BlockchainAppendException
from .block import Block
from .genesis_block import GenesisBlock


class Blockchain:
  def __init__(self):
    self.chain = [self.create_genesis_block()]

  def create_genesis_block(self):
    return Block(GenesisBlock(), VOID_HASH_PTR)

  def add_block_with_data(self, data):
    new_block = Block(data, self.chain[-1].hash)

    # Difficulty level of 4
    new_block.mine_block()
    self.chain.append(new_block)

  def try_append(self, block: Block):
    print("calculating hash of block")
    if not block.previous_hash == self.chain[-1].calculate_hash():
      raise BlockchainAppendException("Attempted to add block with improper prev hash")
    if not block.is_nonce_correct():
      raise BlockchainAppendException("Attempted to add block with improper nonce")
    self.chain.append(block)

  def display_blocks(self):
    print("-" * 30)
    for block in self.chain:
        print(block.to_dict())
        print("-" * 30)
