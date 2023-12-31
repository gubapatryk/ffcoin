from datetime import timezone, timedelta

ENFORCE_PASSWORD_STRENGTH = False

ECC_CURVE = "ed448"
ECC_PROTECTION = "PBKDF2WithHMAC-SHA1AndAES128-CBC"

PRIVATE_KEY_ENCODING = "PEM"
PUBLIC_KEY_ENCODING = "PEM"

SIGNATURE_VERIFIER_MODE = "rfc8032"

BYTE_ENCODING = "utf-8"

LEDGER_PATH = "ledger"
IDENTITY_FILE_NAME = "identity.ffc"
KNOWN_USERS_FILE_NAME = "net.ffc"
EMPTY_KEY_REPRESENTATION = "key not handshook"

INITIAL_TRUSTED_IP = "192.168.195.30"
INITIAL_TRUSTED_NAME = "30"
NON_EXISTENT_IP = "192.168.195.100"
NON_EXISTENT_NAME = ":^]"

IP = "192.168.195.30"
PORT = "1939"
HTTP_TIMEOUT = 10

TIMEZONE = timezone(timedelta(hours=0.0))

MINING_AWARD = 30
INITIAL_BALANCE = 100
MINING_DIFFICULTY = 4
VOID_HASH_PTR = "<NO PREVIOUS HASH>"
GENESIS_BLOCK_TIMESTAMP = -1.0

HTTP_CONSTANTS: dict[str, str] = {
  "SOURCE_IP_HEADER": "Source",
  "NAME_HEADER": "Name",
  "SIGNATURE_HEADER": "Sign",
  "BROADCAST_ID_HEADER": "B-Id"
}

JSON_CONSTANTS: dict[str, str] = {
  "PEERS_KEY": "peers",
  "PUBLIC_KEY_KEY": "publicKey",
  "NAME_KEY": "name",
  "IP_KEY": "ip",
  "SOURCE_IP_KEY": "source",
  "BROADCAST_MESSAGE_ID": "id",
  "FROM_USER_KEY": "from",
  "TO_USER_KEY": "to",
  "TRANSACTION_AMOUNT_KEY": "amount",
  "TRANSACTION_AWARD_KEY": "award",
  "BLOCK_TIMESTAMP_KEY": "timestamp",
  "BLOCK_DATA_KEY": "data",
  "PREVIOUS_HASH_KEY": "prev",
  "BLOCK_NONCE_KEY": "nonce",
  "BLOCK_MINED_BY_KEY": "mined_by",
  "BLOCK_BALANCES_KEY": "balances",
  "GENESIS_BLOCK_COMMENT": "comment"
}

LOCAL_DATA_CONSTANTS: dict[str, str] = {
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
  "User-Agent",
  "Accept-Encoding",
  "Accept",
  "Content-Length",
  "Content-Type",
  "Host",
  HTTP_CONSTANTS["SIGNATURE_HEADER"]
}
