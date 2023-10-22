from Crypto.PublicKey.ECC import EccKey

from constants import INITIAL_TRUSTED_IP, INITIAL_TRUSTED_NAME
from state.user import User
from util.key_util import get_public_key_as_str as stringify_key


class State:

  def __init__(self):
    self.name: str | None = None
    self.private_key: EccKey | None = None
    self.public_key: EccKey | None = None
    self.peers = {
      INITIAL_TRUSTED_IP: User(INITIAL_TRUSTED_NAME, INITIAL_TRUSTED_IP)
    }

  def get_public_key_as_str(self) -> str:
    return stringify_key(self.public_key)

  def add_peer(self, ip: str, user: User):
    old_peer: User | None = self.peers.get(ip)
    if old_peer is None:
      self.peers[ip] = user
    else:
      old_peer.update_with(user)
    return self

  def print_state(self):
    print(f"name: {self.name}")
    print(f"private key: {self.private_key}")
    print(f"public key: {self.public_key}")
    print(f"peers: {self.peers}")


state = State()
