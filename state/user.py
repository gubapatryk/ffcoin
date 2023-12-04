from copy import copy

from Crypto.PublicKey.ECC import EccKey

from constants import JSON_CONSTANTS, EMPTY_KEY_REPRESENTATION
from util.key_util import get_public_key_as_str as stringify_key, str_to_public_key_or_none


class User:

  def __init__(
    self,
    name: str,
    ip: str,
    public_key: "EccKey | None" = None
  ):
    self.name: str = name
    self.ip: str = ip
    self.public_key: "EccKey | None" = public_key

  def get_public_key_as_str(self) -> str:
    return EMPTY_KEY_REPRESENTATION if self.public_key is None else stringify_key(self.public_key)

  def update_with(self, other):
    if self.ip != other.ip:
      raise Exception("Tried to merge users with different ips")
    if (self.public_key is None) or (self.public_key is not None and other.public_key is not None):
      self.name = other.name
      self.public_key = other.public_key
    return self

  def to_dict(self):
    out = {
      JSON_CONSTANTS["NAME_KEY"]: self.name,
      JSON_CONSTANTS["IP_KEY"]: self.ip
    }
    if self.public_key is not None:
      out[JSON_CONSTANTS["PUBLIC_KEY_KEY"]] = self.get_public_key_as_str()
    return out

  def self_without_pk(self):
    out = copy(self)
    out.public_key = None
    return out

  def __str__(self) -> str:
    return f"name: {self.name}, ip: {self.ip}, public_key: {self.get_public_key_as_str()}"


def user_from_dict(d: dict) -> User:

  pub_key_str: str = d[JSON_CONSTANTS["PUBLIC_KEY_KEY"]]

  return User(
    d[JSON_CONSTANTS["NAME_KEY"]],
    d[JSON_CONSTANTS["IP_KEY"]],
    str_to_public_key_or_none(pub_key_str)
  )


def user_from_dict_with_opt_key(d: dict) -> User:
  return user_from_dict(d) if JSON_CONSTANTS["PUBLIC_KEY_KEY"] in d else User(
    d[JSON_CONSTANTS["NAME_KEY"]],
    d[JSON_CONSTANTS["IP_KEY"]]
  )

