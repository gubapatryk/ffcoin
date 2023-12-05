import requests

from requests.exceptions import Timeout, TooManyRedirects, ConnectionError
from constants import MINING_AWARD, HTTP_CONSTANTS, IP, PORT
from state import State
from state.block import Block
from state.transaction import Transaction
from util.broadcast_util import broadcast_id
from util.exception.ip_does_not_exist_exception import IpDoesNotExistException
from util.signing import get_request_signature


def commit_transaction(state: State):
  ip = input("Transaction to: ").strip()
  amount = float(input("Amount: ").strip())
  # verify if has enough funds
  if ip not in state.peers:
    raise IpDoesNotExistException(ip)
  transaction = Transaction(state.as_user().self_without_pk(), state.peers[ip].self_without_pk(), amount, MINING_AWARD)
  block = Block(transaction, state.get_last_hash())
  headers = {
            HTTP_CONSTANTS["SOURCE_IP_HEADER"]: IP,
            HTTP_CONSTANTS["NAME_HEADER"]: state.name,
            HTTP_CONSTANTS["BROADCAST_ID_HEADER"]: broadcast_id()
          }
  signature = get_request_signature(state, block.to_dict(), headers)
  headers[HTTP_CONSTANTS["SIGNATURE_HEADER"]] = signature
  for ip, user in state.peers.copy().items():
    # no check if ip != IP - this should allow the host to mine
    try:
      requests.post(
        f"http://{ip}:{PORT}/transfer",
        headers=headers,
        json=block
      )
    except (ConnectionError, Timeout, TooManyRedirects):
      state.remove_peer(ip)
  # allow host to mine as well pre-broadcast
