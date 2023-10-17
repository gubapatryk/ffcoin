import json

import grequests
import requests

from constants import HTTP_CONSTANTS, PORT, JSON_CONSTANTS, IP
from flask_app import flask_app
from flask import request, Response

from state import state
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
    for peer, ip in state.peers.items():
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
  state.peers[original_name] = original_source_ip
  return sign_response(state, Response(out))


def greet_outcome(state):
  out = state.peers.copy()
  out[state.name] = IP
  return json.dumps({
    JSON_CONSTANTS["PEERS_KEY"]: out
  })


# TODO: rethink saving trusted/untrusted data
# maybe identity should be with keys not names
def optionally_trust_source(state, original_name, original_source_ip):
  known_ip = state.peers.get(original_name)
  if known_ip is not None and known_ip is not original_source_ip:
    pass # verify
  elif known_ip is None:
    state.peers[original_name] = original_source_ip
  # if known_ip is not None and known_ip is original_source_ip
  # do nothing
