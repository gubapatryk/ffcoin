from Crypto.PublicKey import ECC
from Crypto.PublicKey.ECC import EccKey

from constants import PUBLIC_KEY_ENCODING, EMPTY_KEY_REPRESENTATION, ECC_CURVE


def get_public_key_as_str(key: EccKey) -> str:
  return key.export_key(format=PUBLIC_KEY_ENCODING)


def str_to_public_key_or_none(s: str) -> "EccKey | None":
  return None if s == EMPTY_KEY_REPRESENTATION else ECC.import_key(s, ECC_CURVE)
