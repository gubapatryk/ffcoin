import json
from typing import BinaryIO

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.PublicKey import ECC
from Crypto.Random import get_random_bytes

from constants import LEDGER_PATH, IDENTITY_FILE_NAME, \
  PRIVATE_KEY_ENCODING, ECC_CURVE, ECC_PROTECTION, BYTE_ENCODING, \
  LOCAL_DATA_CONSTANTS
from util.b64 import str_to_bytes, b64_encode_bytes, b64_str_to_bytes
from util.password_strength import try_password_strength


def set_up_keys(state):
  name = input("What's your name: ").strip()
  pass1 = input("Create a password for keys: ").strip()
  try_password_strength(pass1)
  pass2 = input("Repeat password: ").strip()
  if pass1 != pass2:
    print("Passwords don't match")
  else:
    save_key(state, pass1, name)


def save_key(state, passphrase, name):

  print("Generating keys...")

  key_pair = ECC.generate(curve=ECC_CURVE)

  private_key_str = key_pair.export_key(format=PRIVATE_KEY_ENCODING, passphrase=passphrase, protection=ECC_PROTECTION)

  print("Saving keys...")

  with open(f"{LEDGER_PATH}/{IDENTITY_FILE_NAME}", 'wb') as f:
    write_key(private_key_str, passphrase, name, f)

  print("Loading keys...")

  load_keys_to_memory(state, key_pair, name)


def write_key(key_str: str, passphrase: str, name: str, f: BinaryIO) -> None:
  dek = get_random_bytes(32)
  dek_nonce = get_random_bytes(16)
  cipher = AES.new(dek, AES.MODE_GCM, nonce=dek_nonce)
  ciphertext = cipher.encrypt(str_to_bytes(key_str))
  salt = b64_encode_bytes(get_random_bytes(32))
  kek = scrypt(passphrase, salt, 32, N=2**20, r=8, p=1)
  kek_nonce = get_random_bytes(16)
  cipher = AES.new(kek, AES.MODE_GCM, nonce=kek_nonce)
  enc_dek = cipher.encrypt(dek)
  out = {
    LOCAL_DATA_CONSTANTS["SALT_KEY"]: salt,
    LOCAL_DATA_CONSTANTS["ENCRYPTED_DEK_KEY"]: b64_encode_bytes(enc_dek),
    LOCAL_DATA_CONSTANTS["CIPHERTEXT_KEY"]: b64_encode_bytes(ciphertext),
    LOCAL_DATA_CONSTANTS["NAME_KEY"]: name,
    LOCAL_DATA_CONSTANTS["KEK_NONCE_NAME"]: b64_encode_bytes(kek_nonce),
    LOCAL_DATA_CONSTANTS["DEK_NONCE_NAME"]: b64_encode_bytes(dek_nonce),
  }
  f.write(str_to_bytes(json.dumps(out)))


def load_keys_to_memory(state, key_pair, name):

  state.name = name
  state.private_key = key_pair
  state.public_key = key_pair.public_key()

  print("OK")


def load_keys(state):
  passphrase = input("Input passphrase: ").strip()

  try:

    print("Loading keys...")

    with open(f"{LEDGER_PATH}/{IDENTITY_FILE_NAME}", 'rb') as f:

      data = json.loads(f.read().decode(BYTE_ENCODING))
      salt = data[LOCAL_DATA_CONSTANTS["SALT_KEY"]]
      enc_dek = data[LOCAL_DATA_CONSTANTS["ENCRYPTED_DEK_KEY"]]
      ciphertext = data[LOCAL_DATA_CONSTANTS["CIPHERTEXT_KEY"]]
      name = data[LOCAL_DATA_CONSTANTS["NAME_KEY"]]
      b64_kek_nonce = data[LOCAL_DATA_CONSTANTS["KEK_NONCE_NAME"]]
      b64_dek_nonce = data[LOCAL_DATA_CONSTANTS["DEK_NONCE_NAME"]]

      kek_nonce = b64_str_to_bytes(b64_kek_nonce)
      dek_nonce = b64_str_to_bytes(b64_dek_nonce)
      kek = scrypt(passphrase, salt, 32, N=2 ** 20, r=8, p=1)
      cipher = AES.new(kek, AES.MODE_GCM, nonce=kek_nonce)
      dek = cipher.decrypt(b64_str_to_bytes(enc_dek))
      cipher = AES.new(dek, AES.MODE_GCM, nonce=dek_nonce)
      padded_key = cipher.decrypt(b64_str_to_bytes(ciphertext)).decode(BYTE_ENCODING)
      key_pair = ECC.import_key(padded_key, passphrase, ECC_CURVE)

      load_keys_to_memory(state, key_pair, name)

  except ValueError:
    print("Invalid password")
