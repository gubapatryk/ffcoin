import hashlib
import datetime
import time


class Block: 
    def __init__(self, data, previous_hash): 

        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash 
        self.nonce = 0
        self.hash = self.calculate_hash() 
  
    def calculate_hash(self): 

        sha = hashlib.sha256() 
        sha.update(str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') + 
                   str(self.previous_hash).encode('utf-8') + 
                   str(self.nonce).encode('utf-8')) 
        return str(sha.hexdigest())
  
    def mine_block(self, difficulty): 

        while self.hash[0:difficulty] != "0" * difficulty: 
            self.nonce += 1
            self.hash = self.calculate_hash() 
  
        print("Block mined:", self.hash)

