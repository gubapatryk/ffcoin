ENFORCE_PASSWORD_STRENGTH = False

ECC_CURVE = "P-256"
ECC_PROTECTION = "PBKDF2WithHMAC-SHA1AndAES128-CBC"

PRIVATE_KEY_ENCODING = "PEM"
PUBLIC_KEY_ENCODING = "PEM"

SIGNATURE_VERIFIER_MODE = "fips-186-3"

BYTE_ENCODING = "utf-8"

LEDGER_PATH = "ledger"
IDENTITY_FILE_NAME = "identity.ffc"
PUBLIC_KEY_FILE_NAME = "key.pub"
USER_DATA_FILE_NAME = "user.data"
IV_FILE_NAME = "iv.aes"

INITIAL_TRUSTED_IP = "192.168.195.30"
INITIAL_TRUSTED_NAME = "30"

IP = "localhost"
PORT = "1939"

HTTP_CONSTANTS = {
  "SOURCE_IP_HEADER": "source",
  "NAME_HEADER": "name",
  "SIGNATURE_HEADER": "sign"
}

JSON_CONSTANTS = {
  "PEERS_KEY": "peers",
  "PUBLIC_KEY_KEY": "publicKey",
  "NAME_KEY": "name",
  "IP_KEY": "ip"
}

LOCAL_DATA_CONSTANTS = {
  "SALT_KEY": "salt",
  "ENCRYPTED_DEK_KEY": "dek",
  "CIPHERTEXT_KEY": "ciphertext",
  "NAME_KEY": "name",
  "KEK_NONCE_NAME": "kek_nonce",
  "DEK_NONCE_NAME": "dek_nonce"
}

NON_SIGNABLE_HEADERS: set[str] = {
  "Server",
  "Date",
  "Connection",
  HTTP_CONSTANTS["SIGNATURE_HEADER"]
}
