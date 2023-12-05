from util.exception.blockchain_append_exception import BlockchainAppendException
from .block import Block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self): 

        return Block("Genesis Block", "0") 
  
    def add_block_with_data(self, data): 
        new_block = Block(data, self.chain[-1].hash) 
          
        # Difficulty level of 4 
        new_block.mine_block()
        self.chain.append(new_block)

    def try_append(self, block: Block):
        if not block.previous_hash == self.chain[-1].calculate_hash():
            raise BlockchainAppendException("Attempted to add block with improper prev hash")
        if not block.is_nonce_correct():
            raise BlockchainAppendException("Attempted to add block with improper nonce")
        self.chain.append(block)

    def display_blocks(self):
        for block in self.chain:
            print(f"Timestamp: {block.timestamp}")
            print(f"Transaction Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print("-" * 30)
