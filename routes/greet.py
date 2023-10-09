import json

import grequests

from constants import HTTP_CONSTANTS, PORT, JSON_CONSTANTS
from flask_app import flask_app
from flask import request

from state import state


# it could be beneficial to store greeted and non-greeted ips
# this way calling this multiple times would lead to a nice greedy discovery algorithm
@flask_app.route("/greet", methods=["POST"])
def greet():
  source_ip = request.headers.get(HTTP_CONSTANTS["SOURCE_IP_HEADER"])
  out = greet_outcome(state)
  if source_ip not in state.peers:
    # async - I suspect waiting for outcome from entire net will fry processors
    for peer in state.peers:
      grequests.post(
        f"http://{peer}:{PORT}/greet",
        headers={
          HTTP_CONSTANTS["SOURCE_IP_HEADER"]: source_ip
        }
      )
    # should we save ips only from sources we already know/trust
    state.peers.add(source_ip)
  print(out) # debug
  return out


def greet_outcome(state):
  return json.dumps({
    JSON_CONSTANTS["PEERS_KEY"]: state.peers
  })
