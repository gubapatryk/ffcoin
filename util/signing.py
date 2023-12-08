import json

from Crypto.Hash import SHAKE256
from Crypto.PublicKey.ECC import EccKey
from Crypto.Signature import eddsa
from requests import Response as InResponse
from flask import Response as OutResponse, Request

from constants import SIGNATURE_VERIFIER_MODE, HTTP_CONSTANTS, NON_SIGNABLE_HEADERS
from state import State
from util.b64 import b64_encode_bytes, str_to_bytes, b64_str_to_bytes
from util.exception.signature_exception import SignatureException


def sign(state: State, bstr: bytes) -> str:
  hash = SHAKE256.new(bstr)
  signer = eddsa.new(state.private_key, SIGNATURE_VERIFIER_MODE)
  return b64_encode_bytes(signer.sign(hash))


def sign_response(state, resp: OutResponse) -> OutResponse:
  header = sign(state, out_response_to_bytes(resp))
  resp.headers[HTTP_CONSTANTS["SIGNATURE_HEADER"]] = header
  return resp


def get_request_signature(state: State, body: dict, headers: dict) -> str:
  input = str_to_bytes(json.dumps(body) + headers_to_str(headers))
  return sign(state, input)


def verify(pub_key: EccKey, payload: bytes, signature: str):
  hsh = SHAKE256.new(payload)
  verifier = eddsa.new(pub_key, SIGNATURE_VERIFIER_MODE)
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


def verify_request(pub_key: EccKey, request: Request) -> bool:
  signature = request.headers[HTTP_CONSTANTS["SIGNATURE_HEADER"]]
  input: bytes = str_to_bytes(request.get_data(as_text=True) + headers_to_str(request.headers))
  return verify(pub_key, input, signature)


def try_verify_response(state: State, ip: str, response: InResponse):
  pub_key: EccKey = state.peers[ip].public_key
  signature = response.headers[HTTP_CONSTANTS["SIGNATURE_HEADER"]]
  return try_verify(pub_key, in_response_to_bytes(response), signature)


def in_response_to_bytes(response: InResponse) -> bytes:
  body_str = response.text
  headers_str = ",".join([
    f"{key}:{value}" for key, value in filter_non_signable_headers(response.headers)
  ])
  return str_to_bytes(body_str + headers_str)


def out_response_to_bytes(response: OutResponse) -> bytes:
  body_str = response.get_data(as_text=True)
  headers_str = headers_to_str(response.headers)
  return str_to_bytes(body_str + headers_str)


def headers_to_str(headers) -> str:
  return ",".join([
    f"{key}:{value}" for key, value in filter_non_signable_headers(headers)
  ])


def filter_non_signable_headers(headers) -> list:
  # refactor this to getting list of signeable headers from headers
  non_signeable_headers = set(map(lambda v: v.upper(), NON_SIGNABLE_HEADERS))
  filtered_headers = filter(lambda tpl: tpl[0].upper() not in non_signeable_headers, headers.items())
  sorted_headers = list(filtered_headers)
  sorted_headers.sort(key=lambda tpl: tpl[0])
  return sorted_headers
