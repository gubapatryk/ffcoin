import json

from constants import INITIAL_TRUSTED_IP, INITIAL_TRUSTED_NAME, \
  NON_EXISTENT_IP, NON_EXISTENT_NAME, JSON_CONSTANTS, \
  EMPTY_KEY_REPRESENTATION, LEDGER_PATH, KNOWN_USERS_FILE_NAME, BYTE_ENCODING, IP, INITIAL_BALANCE
from state.balance import Balance, BalanceEntry
from state.block import Block
from state.broadcast_entry import BroadcastEntry
from state.user import User, user_from_dict
from util.key_util import get_public_key_as_str as stringify_key

from state.blockchain import Blockchain
from util.state_util import parse_peer_list


class State:

  def __init__(self):
    self.name: "str | None" = None
    self.private_key: "EccKey | None" = None
    self.public_key: "EccKey | None" = None
    self.peers: dict[str, User] = {
      INITIAL_TRUSTED_IP: User(INITIAL_TRUSTED_NAME, INITIAL_TRUSTED_IP),
      NON_EXISTENT_IP: User(NON_EXISTENT_NAME, NON_EXISTENT_IP)
    }
    self.broadcast_table: dict[str, BroadcastEntry] = dict()
    self.blockchain = Blockchain()
    self.hostile_mode = False

  def get_public_key_as_str(self) -> str:
    return EMPTY_KEY_REPRESENTATION if self.public_key is None else stringify_key(self.public_key)

  def get_last_hash(self) -> str:
    return self.blockchain.chain[-1].calculate_hash()

  def get_peers_list(self):
    return parse_peer_list(list(self.peers.copy().items()))

  def add_peer(self, ip: str, user: User):
    old_peer: "User | None" = self.peers.get(ip)
    if old_peer is None:
      self.peers[ip] = user
    else:
      old_peer.update_with(user)
    return self

  def remove_peer(self, ip: str, with_message: bool = True):
    if with_message:
      print(f"Removing user {ip} due to connection error")
    self.peers.pop(ip)

  def calculate_balances(self) -> Balance:
    return Balance(self.blockchain)

  def get_self_balance(self) -> BalanceEntry:
    self_balance = self.calculate_balances().balance.get(IP)
    return self_balance if self_balance is not None else BalanceEntry(self.as_user(), INITIAL_BALANCE)

  def try_can_block_be_added_to_blockchain(self, block: Block) -> None:
    self.blockchain.try_can_block_be_added_to_blockchain(block)

  def add_broadcast_entry(self, id: str):
    self.broadcast_table[id] = BroadcastEntry(id)
    return self

  def peers_to_save_dict(self) -> dict:
    return {
      JSON_CONSTANTS["PEERS_KEY"]: [user.to_dict() for user in self.peers.values()]
    }

  def override_peers_from_dict(self, d: dict):
    peers_l: list = [user_from_dict(peer_dict) for peer_dict in d[JSON_CONSTANTS["PEERS_KEY"]]]
    self.peers = {user.ip: user for user in peers_l}
    return self

  def save_peers_to_file(self) -> None:
    with open(f"{LEDGER_PATH}/{KNOWN_USERS_FILE_NAME}", 'wb') as f:
      data = json.dumps(self.peers_to_save_dict()).encode(BYTE_ENCODING)
      f.write(data)

  def print_state(self):
    print(f"name: {self.name}")
    print(f"private key: ???")
    print(f"public key: {self.get_public_key_as_str()}")
    for ip, peer in self.peers.items():
      print(peer)
    self.blockchain.display_blocks()
    print("Balance")
    print(self.calculate_balances())

  def as_user(self):
    return User(self.name, IP, self.public_key)


state = State()
