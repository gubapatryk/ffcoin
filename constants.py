from datetime import timezone, timedelta

ENFORCE_PASSWORD_STRENGTH = False

ECC_CURVE = "P-256"
ECC_PROTECTION = "PBKDF2WithHMAC-SHA1AndAES128-CBC"

PRIVATE_KEY_ENCODING = "PEM"
PUBLIC_KEY_ENCODING = "PEM"

SIGNATURE_VERIFIER_MODE = "fips-186-3"

BYTE_ENCODING = "utf-8"

LEDGER_PATH = "ledger"
IDENTITY_FILE_NAME = "identity.ffc"
KNOWN_USERS_FILE_NAME = "net.ffc"
EMPTY_KEY_REPRESENTATION = "key not handshook"

INITIAL_TRUSTED_IP = "192.168.195.30"
INITIAL_TRUSTED_NAME = "30"
NON_EXISTENT_IP = "192.168.195.100"
NON_EXISTENT_NAME = ":^]"

IP = "localhost"
PORT = "1939"
HTTP_TIMEOUT = 10

TIMEZONE = timezone(timedelta(hours=0.0))

HTTP_CONSTANTS = {
  "SOURCE_IP_HEADER": "source",
  "NAME_HEADER": "name",
  "SIGNATURE_HEADER": "sign",
}

JSON_CONSTANTS = {
  "PEERS_KEY": "peers",
  "PUBLIC_KEY_KEY": "publicKey",
  "NAME_KEY": "name",
  "IP_KEY": "ip",
  "SOURCE_IP_KEY": "source",
  "BROADCAST_MESSAGE_ID": "id"
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
