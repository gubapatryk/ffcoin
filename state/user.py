from Crypto.PublicKey.ECC import EccKey

from util.key_util import get_public_key_as_str as stringify_key


class User:

  def __init__(
    self,
    name: "str | None" = None,
    ip: "str | None" = None,
    public_key: "EccKey | None" = None
  ):
    self.name: "str | None" = name
    self.ip: "str | None" = ip
    self.public_key: "EccKey | None" = public_key

  def get_public_key_as_str(self) -> str:
    return stringify_key(self.public_key)

  def update_with(self, other):
    print("self.ip")
    print(self.ip)
    print("other.ip")
    print(other.ip)
    if self.ip == other.ip:
      raise Exception("Tried to merge users with different ips")
    if (self.public_key is None) or (self.public_key is not None and other.public_key is not None):
      self.name = other.name
      self.public_key = other.public_key
    return self

  def __str__(self) -> str:
    return f"name: {self.name}, ip: {self.ip}, public_key: {self.public_key}"

