import json

from Crypto.Hash import SHA256
from Crypto.Signature import DSS

from constants import SIGNATURE_VERIFIER_MODE
from util.b64 import b64_encode_bytes, str_to_bytes, b64_str_to_bytes


def sign(state, str):
  hash = SHA256.new(str_to_bytes(str))
  signer = DSS.new(state.private_key, SIGNATURE_VERIFIER_MODE)
  return b64_encode_bytes(signer.sign(hash))


def sign_dict(state, dict_payload):
  sign(state, json.dumps(dict_payload))


def verify(pub_key, payload, signature):
  hash = SHA256.new(str_to_bytes(payload))
  verifier = DSS.new(pub_key, SIGNATURE_VERIFIER_MODE)
  try:
    verifier.verify(hash, b64_str_to_bytes(signature))
    return True
  except ValueError:
    return False


def verify_dict(pub_key, payload, signature):
  verify(pub_key, json.dumps(payload), signature)
