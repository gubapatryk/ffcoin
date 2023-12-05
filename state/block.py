import hashlib
import time
from random import randint

from constants import JSON_CONSTANTS, MINING_DIFFICULTY
from state.transaction import transaction_from_dict
from state.user import user_from_dict_with_opt_key


class Block:
  def __init__(self, data, previous_hash, t=None, nonce=0, mined_by=None):
    self.timestamp = time.time() if t is None else t
    self.data = data
    self.previous_hash = previous_hash
    self.nonce = nonce
    self.hash = self.calculate_hash()
    self.mined_by = mined_by

  def __eq__(self, other):
    if isinstance(other, Block):
      return self.timestamp == other.timestamp and self.previous_hash == other.previous_hash and self.data == other.data
    return False

  def calculate_hash(self):

    sha = hashlib.sha256()
    sha.update(str(self.timestamp).encode('utf-8') +
      str(self.data.to_dict()).encode('utf-8') +
      str(self.previous_hash).encode('utf-8') +
      str(self.nonce).encode('utf-8'))
    return str(sha.hexdigest())

  def mine_block(self, difficulty=MINING_DIFFICULTY):

    retries = 0
    max_range = 2**24
    self.nonce = randint(0, max_range)
    self.hash = self.calculate_hash()

    while self.hash[0:difficulty] != "0" * difficulty:
      self.nonce = randint(0, max_range)
      self.hash = self.calculate_hash()
      retries = retries + 1
      if 2 * retries > max_range:
        max_range = 2 * max_range

    return self

  def is_nonce_correct(self, difficulty=MINING_DIFFICULTY) -> bool:
    hsh = self.calculate_hash()
    return hsh[0:difficulty] == "0" * difficulty

  def to_dict(self):
    out = {
      JSON_CONSTANTS["BLOCK_TIMESTAMP_KEY"]: self.timestamp,
      JSON_CONSTANTS["BLOCK_DATA_KEY"]: self.data.to_dict(),
      JSON_CONSTANTS["PREVIOUS_HASH_KEY"]: self.previous_hash,
      JSON_CONSTANTS["BLOCK_NONCE_KEY"]: self.nonce,
    }
    if self.mined_by is not None:
      out[JSON_CONSTANTS["BLOCK_MINED_BY_KEY"]] = self.mined_by.to_dict(with_pk=False)
    return out


def block_from_dict(d: dict) -> Block:
  transaction_d = d[JSON_CONSTANTS["BLOCK_DATA_KEY"]]
  tmstmp = d[JSON_CONSTANTS["BLOCK_TIMESTAMP_KEY"]]
  prev_hash = d[JSON_CONSTANTS["PREVIOUS_HASH_KEY"]]
  nonce = d.get(JSON_CONSTANTS["BLOCK_NONCE_KEY"])
  nonce = 0 if nonce is None else nonce
  mined_by = d.get(JSON_CONSTANTS["BLOCK_MINED_BY_KEY"])
  mined_by = None if mined_by is None else user_from_dict_with_opt_key(mined_by)

  return Block(transaction_from_dict(transaction_d), prev_hash, tmstmp, nonce, mined_by)

