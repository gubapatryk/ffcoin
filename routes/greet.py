import json

import grequests
import requests

from constants import HTTP_CONSTANTS, PORT, JSON_CONSTANTS, IP
from flask_app import flask_app
from flask import request

from state import state


# it could be beneficial to store greeted and non-greeted ips
# this way calling this multiple times would lead to a nice greedy discovery algorithm
@flask_app.route("/greet", methods=["POST"])
def greet():
  original_source_ip = request.headers.get(HTTP_CONSTANTS["SOURCE_IP_HEADER"])
  direct_source_ip = request.remote_addr
  out = greet_outcome(state)
  if original_source_ip not in state.peers and direct_source_ip not in state.peers:
    # async - I suspect waiting for outcome from entire net will fry processors
    for peer in state.peers:
      if peer is not IP:
        requests.post(  # TODO: make it async
          f"http://{peer}:{PORT}/greet",
          headers={
            HTTP_CONSTANTS["SOURCE_IP_HEADER"]: original_source_ip
          }
        )
  # should we save ips only from sources we already know/trust
  state.peers.add(original_source_ip)
  return out


def greet_outcome(state):
  out = state.peers.copy()
  out.add(IP)
  return json.dumps({
    JSON_CONSTANTS["PEERS_KEY"]: list(out)
  })
