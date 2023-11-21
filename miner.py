import random
import string

class Miner:
    def __init__(self, blockchain):
        self.blockchain = blockchain

#    def mine_blocks(self):
#        while True:
#            random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
#            self.blockchain.add_block_with_data(random_data)
#            print(f"Mined new block with data: {random_data}")
#        print("\n\n\n\nSTAN LANCUCHA BLOKOW:")
#        self.blockchain.display_blocks()
