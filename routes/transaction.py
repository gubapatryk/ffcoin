import requests
from flask import request

from requests.exceptions import Timeout, TooManyRedirects, ConnectionError
from constants import HTTP_CONSTANTS, IP, PORT
from flask_app import flask_app
from state import state
from state.block import block_from_dict
from util.broadcast_util import broadcast_id
from util.exception.blockchain_append_exception import BlockchainAppendException
from util.signing import verify_request, get_request_signature


@flask_app.route("/transfer", methods=["POST"])
def transfer():
  direct_source_ip = request.remote_addr
  data: dict = request.get_json()
  headers: dict = request.headers
  message_id = headers[HTTP_CONSTANTS["BROADCAST_ID_HEADER"]]
  original_source_ip = headers[HTTP_CONSTANTS["SOURCE_IP_HEADER"]]
  original_name = headers[HTTP_CONSTANTS["NAME_HEADER"]]
  signature = headers[HTTP_CONSTANTS["SIGNATURE_HEADER"]]
  if original_source_ip not in state.peers:
    print("Peer is not discovered - transaction will not be mined")
    return {}
  source_pub_key = state.peers.get(original_source_ip).public_key
  if source_pub_key is None:
    print("PubKey of peer is not stored - consider handshaking")  # we also could perform handshake here but I cba
    return {}
  if not verify_request(source_pub_key, request):
    print("The signature of received transfer is invalid")
    return "The signature of received transfer is invalid", 403
  block = block_from_dict(data)
  state.try_can_block_be_added_to_blockchain(block)
  # end of prep
  if message_id not in state.broadcast_table:
    for ip, peer in state.get_peers_list():
      if ip != IP and ip != direct_source_ip and ip != original_source_ip:
        try:
          requests.post(  # TODO: make it async
            f"http://{ip}:{PORT}/transfer", json=data, headers={
              HTTP_CONSTANTS["SOURCE_IP_HEADER"]: original_source_ip,
              HTTP_CONSTANTS["NAME_HEADER"]: original_name,
              HTTP_CONSTANTS["BROADCAST_ID_HEADER"]: message_id,
              HTTP_CONSTANTS["SIGNATURE_HEADER"]: signature
            })
        except (ConnectionError, Timeout, TooManyRedirects):
          state.remove_peer(ip)
    block.mine_block()
    try:
      state.blockchain.try_append(block)
      block.mined_by = state.as_user()  # passed to blockchain by reference
      # since we were able to add to local blockchain means we could be first
      data = block.to_dict()
      headers = {
                HTTP_CONSTANTS["SOURCE_IP_HEADER"]: IP,
                HTTP_CONSTANTS["NAME_HEADER"]: state.name,
                HTTP_CONSTANTS["BROADCAST_ID_HEADER"]: broadcast_id()
              }
      signature = get_request_signature(state, data, headers)
      headers[HTTP_CONSTANTS["SIGNATURE_HEADER"]] = signature
      for ip, peer in state.get_peers_list():
        if ip != IP:
          try:
            requests.post(  # TODO: make it async
              f"http://{ip}:{PORT}/declare-block", json=data, headers=headers)
          except (ConnectionError, Timeout, TooManyRedirects):
            state.remove_peer(ip)
    except BlockchainAppendException as e:
      print(e.msg)
      return {}
  return {}
