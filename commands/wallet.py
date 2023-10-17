from Crypto.Cipher import AES
from Crypto.PublicKey import RSA, ECC
from Crypto.Util.Padding import pad, unpad

from constants import KEY_SIZE, CRYPTO_EXPONENT, PUBLIC_KEY_ENCODING, LEDGER_PATH, PRIVATE_KEY_FILE_NAME, \
  PUBLIC_KEY_FILE_NAME, PRIVATE_KEY_ENCODING, USER_DATA_FILE_NAME, ECC_CURVE, ECC_PROTECTION, BYTE_ENCODING, \
  IV_FILE_NAME
from util.b64 import str_to_bytes


def set_up_keys(state):
  name = input("What's your name: ").strip()
  pass1 = input("Create a password for keys: ").strip()
  pass2 = input("Repeat password: ").strip()
  if pass1 != pass2:
    print("Passwords don't match")
  else:
    save_key(state, pass1, name)


def save_key(state, passphrase, name):

  print("Generating keys...")

  key_pair = ECC.generate(curve=ECC_CURVE)

  private_key_str = key_pair.export_key(format=PRIVATE_KEY_ENCODING, passphrase=passphrase, protection=ECC_PROTECTION)

  public_key_str = key_pair.public_key().export_key(format=PUBLIC_KEY_ENCODING)

  with open(f"{LEDGER_PATH}/{IV_FILE_NAME}", 'rb') as f:
    iv = f.read()

  print("Saving keys...")

  with open(f"{LEDGER_PATH}/{PRIVATE_KEY_FILE_NAME}", 'wb') as f:
    write_key(private_key_str, passphrase, iv, f)

  with open(f"{LEDGER_PATH}/{PUBLIC_KEY_FILE_NAME}", 'wb') as f:
    write_key(public_key_str, passphrase, iv, f)

  with open(f"{LEDGER_PATH}/{USER_DATA_FILE_NAME}", 'w') as f:
    f.write(name)

  print("Loading keys...")

  load_keys_to_memory(state, key_pair, name)


def write_key(key_str, passphrase, iv, f):
  passphrase = pad(str_to_bytes(passphrase), AES.block_size)
  cipher = AES.new(passphrase, AES.MODE_CBC, iv=iv)
  out = cipher.encrypt(pad(str_to_bytes(key_str), AES.block_size))
  f.write(out)


def load_keys_to_memory(state, key_pair, name):

  state.name = name
  state.private_key = key_pair
  state.public_key = key_pair.public_key()

  print("OK")


def load_keys(state):
  passphrase = input("Input passphrase: ").strip()

  try:

    print("Loading keys...")

    with open(f"{LEDGER_PATH}/{IV_FILE_NAME}", 'rb') as f:
      iv = f.read()

    with open(f"{LEDGER_PATH}/{PRIVATE_KEY_FILE_NAME}", 'rb') as f:
      b_passphrase = pad(str_to_bytes(passphrase), AES.block_size)
      cipher = AES.new(b_passphrase, AES.MODE_CBC, iv)
      inp = unpad(cipher.decrypt(f.read()), AES.block_size)
      key_pair = ECC.import_key(inp.decode(BYTE_ENCODING), passphrase, ECC_CURVE)

    with open(f"{LEDGER_PATH}/{USER_DATA_FILE_NAME}", 'r') as f:
      name = f.read().strip()

    load_keys_to_memory(state, key_pair, name)

  except ValueError:
    print("Invalid passphrase")
