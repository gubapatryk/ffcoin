import json

from Crypto.PublicKey.ECC import EccKey

from constants import INITIAL_TRUSTED_IP, INITIAL_TRUSTED_NAME, ADDITIONAL_TRUSTED_IP, ADDITIONAL_TRUSTED_NAME, NON_EXISTENT_IP, NON_EXISTENT_NAME, JSON_CONSTANTS, \
  EMPTY_KEY_REPRESENTATION, LEDGER_PATH, KNOWN_USERS_FILE_NAME, BYTE_ENCODING
from state.broadcast_entry import BroadcastEntry
from state.user import User, user_from_dict
from util.key_util import get_public_key_as_str as stringify_key

from state.blockchain import Blockchain


class State:

  def __init__(self):
    self.name: "str | None" = None
    self.private_key: "EccKey | None" = None
    self.public_key: "EccKey | None" = None
    self.peers: dict[str, User] = {
      INITIAL_TRUSTED_IP: User(INITIAL_TRUSTED_NAME, INITIAL_TRUSTED_IP),
      ADDITIONAL_TRUSTED_IP: User(INITIAL_TRUSTED_NAME, ADDITIONAL_TRUSTED_NAME),
      NON_EXISTENT_IP: User(NON_EXISTENT_NAME, NON_EXISTENT_IP)
    }
    self.broadcast_table: dict[str, BroadcastEntry] = dict()
    self.blockchain = Blockchain()
    self.hostile_mode = False

  def get_public_key_as_str(self) -> str:
    return EMPTY_KEY_REPRESENTATION if self.public_key is None else stringify_key(self.public_key)

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


state = State()
