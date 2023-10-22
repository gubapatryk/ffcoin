import json

import requests

from constants import HTTP_CONSTANTS, PORT, JSON_CONSTANTS, IP
from flask_app import flask_app
from flask import request, Response

from state import state, State, User
from util.signing import sign_response


# it could be beneficial to store greeted and non-greeted ips
# this way calling this multiple times would lead to a nice greedy discovery algorithm
@flask_app.route("/greet", methods=["POST"])
def greet():
  original_source_ip = request.headers.get(HTTP_CONSTANTS["SOURCE_IP_HEADER"])
  original_name = request.headers.get(HTTP_CONSTANTS["NAME_HEADER"])
  direct_source_ip = request.remote_addr
  out = greet_outcome(state)
  if original_source_ip not in state.peers.values() and direct_source_ip not in state.peers.values():
    # async - I suspect waiting for outcome from entire net will fry processors
    for ip, peer in state.peers.copy().items():
      if ip is not IP:
        requests.post(  # TODO: make it async
          f"http://{ip}:{PORT}/greet",
          headers={
            HTTP_CONSTANTS["SOURCE_IP_HEADER"]: original_source_ip,
            HTTP_CONSTANTS["NAME_HEADER"]: original_name
          }
        )
  # should we save ips only from sources we already know/trust
  # should we override ip?
  greeter_user = User(original_name, original_source_ip)
  state.add_peer(original_source_ip, greeter_user)
  return sign_response(state, Response(out))


def greet_outcome(state: State):

  out = [{
    JSON_CONSTANTS["IP_KEY"]: IP,
    JSON_CONSTANTS["NAME_KEY"]: state.name
  }]

  peer: User
  for ip, peer in state.peers.copy().items():
    out.append({
      JSON_CONSTANTS["IP_KEY"]: ip,
      JSON_CONSTANTS["NAME_KEY"]: peer.name
    })

  return json.dumps({
    JSON_CONSTANTS["PEERS_KEY"]: out
  })
