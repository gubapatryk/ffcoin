from Crypto.Hash import SHA256
from Crypto.PublicKey.ECC import EccKey
from Crypto.Signature import DSS
from requests import Response as InResponse
from flask import Response as OutResponse

from constants import SIGNATURE_VERIFIER_MODE, HTTP_CONSTANTS, NON_SIGNABLE_HEADERS
from state import State
from util.b64 import b64_encode_bytes, str_to_bytes, b64_str_to_bytes
from util.exception.signature_exception import SignatureException


def sign(state: State, bstr: bytes) -> str:
  hash = SHA256.new(bstr)
  signer = DSS.new(state.private_key, SIGNATURE_VERIFIER_MODE)
  return b64_encode_bytes(signer.sign(hash))


def sign_response(state, resp: OutResponse) -> OutResponse:
  header = sign(state, out_response_to_bytes(resp))
  resp.headers[HTTP_CONSTANTS["SIGNATURE_HEADER"]] = header
  return resp


def verify(pub_key: EccKey, payload: bytes, signature: str):
  hsh = SHA256.new(payload)
  verifier = DSS.new(pub_key, SIGNATURE_VERIFIER_MODE)
  try:
    verifier.verify(hsh, b64_str_to_bytes(signature))
    return True
  except ValueError:
    return False


def try_verify(pub_key: EccKey, payload: bytes, signature: str):
  if verify(pub_key, payload, signature):
    return True
  else:
    raise SignatureException()


def try_verify_response(state: State, ip: str, response: InResponse):
  pub_key: EccKey = state.peers[ip].public_key
  signature = response.headers[HTTP_CONSTANTS["SIGNATURE_HEADER"]]
  return try_verify(pub_key, in_response_to_bytes(response), signature)


def in_response_to_bytes(response: InResponse) -> bytes:
  body_str = response.text
  headers_str = ",".join([
    f"{key}:{value}" for key, value in filter_non_signable_headers(response.headers)
  ])
  print("IN response")
  print(body_str + headers_str)
  return str_to_bytes(body_str + headers_str)


def out_response_to_bytes(response: OutResponse) -> bytes:
  body_str = response.get_data(as_text=True)
  headers_str = ",".join([
    f"{key}:{value}" for key, value in filter_non_signable_headers(response.headers)
  ])
  print("OUT response")
  print(body_str + headers_str)
  return str_to_bytes(body_str + headers_str)


def filter_non_signable_headers(headers):
  return filter(lambda tpl: tpl[0] not in NON_SIGNABLE_HEADERS, headers.items())
