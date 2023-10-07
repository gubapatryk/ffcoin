from Crypto.PublicKey import RSA
from constants import KEY_SIZE, CRYPTO_EXPONENT, PUBLIC_KEY_ENCODING, LEDGER_PATH, PRIVATE_KEY_FILE_NAME, \
  PUBLIC_KEY_FILE_NAME, PRIVATE_KEY_ENCODING


def set_up_keys(state):
  pass1 = input("Create a password for keys: ").strip()
  pass2 = input("Repeat password: ").strip()
  if pass1 != pass2:
    print("Passwords don't match")
  else:
    save_key(state, pass1)


def save_key(state, passphrase):

  print("Generating keys...")

  key_pair = RSA.generate(KEY_SIZE, e=CRYPTO_EXPONENT)

  private_key_bytes = key_pair.export_key(PRIVATE_KEY_ENCODING, passphrase)

  public_key_bytes = key_pair.public_key().export_key(PUBLIC_KEY_ENCODING)

  print("Saving keys...")

  with open(f"{LEDGER_PATH}/{PRIVATE_KEY_FILE_NAME}", 'wb') as f:
    f.write(private_key_bytes)

  with open(f"{LEDGER_PATH}/{PUBLIC_KEY_FILE_NAME}", 'wb') as f:
    f.write(public_key_bytes)

  print("Loading keys...")

  load_keys_to_memory(state, key_pair)


def load_keys_to_memory(state, key_pair):

  state.private_key = key_pair
  state.public_key = key_pair.public_key()

  print("OK")


def load_keys(state):
  passphrase = input("Input passphrase: ").strip()

  try:

    print("Loading keys...")

    with open(f"{LEDGER_PATH}/{PRIVATE_KEY_FILE_NAME}", 'rb') as f:
      key_pair = RSA.import_key(f.read(), passphrase)

    load_keys_to_memory(state, key_pair)

  except ValueError:
    print("Invalid passphrase")
