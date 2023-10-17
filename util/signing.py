import json

from Crypto.Hash import SHA256
from Crypto.Signature import DSS

from constants import SIGNATURE_VERIFIER_MODE, HTTP_CONSTANTS
from util.b64 import b64_encode_bytes, str_to_bytes, b64_str_to_bytes
from util.exception.signature_exception import SignatureException


def sign(state, bstr):
  print(bstr)
  hash = SHA256.new(bstr)
  signer = DSS.new(state.private_key, SIGNATURE_VERIFIER_MODE)
  return b64_encode_bytes(signer.sign(hash))


def sign_response(state, resp):
  header = sign(state, resp.response[0])
  resp.headers[HTTP_CONSTANTS["SIGNATURE_HEADER"]] = header
  return resp


def sign_dict(state, dict_payload):
  sign(state, str_to_bytes(json.dumps(dict_payload)))


def verify(pub_key, payload, signature):
  print(payload)
  print(str_to_bytes(payload))
  hash = SHA256.new(str_to_bytes(payload))
  verifier = DSS.new(pub_key, SIGNATURE_VERIFIER_MODE)
  try:
    verifier.verify(hash, b64_str_to_bytes(signature))
    return True
  except ValueError:
    return False


def verify_dict(pub_key, payload, signature):
  verify(pub_key, json.dumps(payload), signature)


def try_verify(pub_key, payload, signature):
  if verify(pub_key, payload, signature):
    return True
  else:
    raise SignatureException()
