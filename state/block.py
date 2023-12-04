import hashlib
import time

from constants import JSON_CONSTANTS


class Block:
  def __init__(self, data, previous_hash, t=None, nonce=0, mined_by=None):
    self.timestamp = time.time() if t is None else t
    self.data = data
    self.previous_hash = previous_hash
    self.nonce = nonce
    self.hash = self.calculate_hash()
    self.mined_by = mined_by

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

  def to_dict(self):
    out = {
      JSON_CONSTANTS["BLOCK_TIMESTAMP_KEY"]: self.timestamp,
      JSON_CONSTANTS["BLOCK_DATA_KEY"]: self.data.to_dict(),
      JSON_CONSTANTS["PREVIOUS_HASH_KEY"]: self.previous_hash,
      JSON_CONSTANTS["BLOCK_NONCE_KEY"]: self.nonce,
    }
    if self.mined_by is not None:
      out[JSON_CONSTANTS["BLOCK_MINED_BY_KEY"]] = self.mined_by.to_dict()
    return out



