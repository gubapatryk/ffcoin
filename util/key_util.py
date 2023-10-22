from Crypto.PublicKey.ECC import EccKey

from constants import PUBLIC_KEY_ENCODING


def get_public_key_as_str(key: EccKey) -> str:
  return key.export_key(format=PUBLIC_KEY_ENCODING)
