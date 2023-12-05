import requests
from flask import request

from requests.exceptions import Timeout, TooManyRedirects, ConnectionError
from constants import HTTP_CONSTANTS, IP, PORT
from flask_app import flask_app
from state import state
from state.block import block_from_dict
from util.exception.blockchain_append_exception import BlockchainAppendException


@flask_app.route("/declare-block", methods=["POST"])
def transfer():
  data: dict = request.get_json()
  headers: dict = request.headers
  source_ip = headers[HTTP_CONSTANTS["SOURCE_IP_HEADER"]]
  source_name = headers[HTTP_CONSTANTS["NAME_HEADER"]]
  message_id = headers[HTTP_CONSTANTS["BROADCAST_ID_HEADER"]]
  signature = headers[HTTP_CONSTANTS["SIGNATURE_HEADER"]]
  if source_ip not in state.peers:
    print("Peer is not discovered - block will not be accepted")
    return {}
  source_pub_key = state.peers.get(source_ip).public_key
  if source_pub_key is None:
    print("PubKey of peer is not stored - block will not be accepted")  # we also could perform handshake here but I cba
    return {}
  block = block_from_dict(data)
  try:
    state.blockchain.try_append(block)
  except BlockchainAppendException as e:  # maybe we still should broadcast even if block cannot be added
    print(e.msg)
    return {}
  for ip, peer in state.peers.copy().items():
    if ip != IP:
      try:
        requests.post(  # TODO: make it async
          f"http://{ip}:{PORT}/declare-block", json=data, headers={
            HTTP_CONSTANTS["SOURCE_IP_HEADER"]: source_ip,
            HTTP_CONSTANTS["NAME_HEADER"]: source_name,
            HTTP_CONSTANTS["BROADCAST_ID_HEADER"]: message_id,
            HTTP_CONSTANTS["SIGNATURE_HEADER"]: signature
          })
      except (ConnectionError, Timeout, TooManyRedirects):
        state.remove_peer(ip)
  return {}
