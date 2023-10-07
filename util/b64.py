import base64

from constants import BYTE_ENCODING


def b64_encode_bytes(bstr):
  return base64.b64encode(bstr).decode(BYTE_ENCODING)


def b64_str_to_bytes(str):
  return base64.b64decode(str.encode())
