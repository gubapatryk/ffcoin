import base64

from constants import BYTE_ENCODING


def b64_encode_bytes(bstr: bytes) -> str:
  return base64.b64encode(bstr).decode(BYTE_ENCODING)


def b64_str_to_bytes(string: str) -> bytes:
  return base64.b64decode(string.encode())


def str_to_bytes(strng: str) -> bytes:
  return bytes(strng, BYTE_ENCODING)
