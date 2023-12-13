import json

import requests
from requests.exceptions import Timeout, TooManyRedirects, ConnectionError

from constants import HTTP_CONSTANTS, PORT, JSON_CONSTANTS, IP
from flask_app import flask_app
from flask import request, Response

from state import state, State, User
from util.signing import sign_response


# deprecated
@flask_app.route("/greet", methods=["POST"])
def greet():
  original_source_ip = request.headers.get(HTTP_CONSTANTS["SOURCE_IP_HEADER"])
  original_name = request.headers.get(HTTP_CONSTANTS["NAME_HEADER"])
  direct_source_ip = request.remote_addr
  out = greet_outcome(state)
  if original_source_ip not in state.peers.keys() and direct_source_ip not in state.peers.keys():
    for ip, peer in state.get_peers_list():
      if ip != IP:
        try:
          requests.post(  # TODO: make it async
            f"http://{ip}:{PORT}/greet",
            headers={
              HTTP_CONSTANTS["SOURCE_IP_HEADER"]: original_source_ip,
              HTTP_CONSTANTS["NAME_HEADER"]: original_name
            }
          )
        except (ConnectionError, Timeout, TooManyRedirects):
          state.remove_peer(ip)
  greeter_user = User(original_name, original_source_ip)
  state.add_peer(original_source_ip, greeter_user)
  return sign_response(state, Response(out))


@flask_app.route("/broadcast", methods=["POST"])
def broadcast():
  direct_source_ip = request.remote_addr
  data: dict = request.get_json()
  message_id = data[JSON_CONSTANTS["BROADCAST_MESSAGE_ID"]]
  original_source_ip = data[JSON_CONSTANTS["SOURCE_IP_KEY"]]
  original_name = data[JSON_CONSTANTS["NAME_KEY"]]
  if message_id not in state.broadcast_table:
    greeter_user = User(original_name, original_source_ip)
    state.add_peer(original_source_ip, greeter_user)
    for ip, peer in state.get_peers_list():
      if ip != IP and ip != direct_source_ip and ip != original_source_ip:
        try:
          requests.post(  # TODO: make it async
            f"http://{ip}:{PORT}/broadcast", json=data
          )
        except (ConnectionError, Timeout, TooManyRedirects):
          state.remove_peer(ip)
    try:
      print(f"poking {original_source_ip}")
      requests.post(
        f"http://{original_source_ip}:{PORT}/poke", json={
          JSON_CONSTANTS["SOURCE_IP_KEY"]: IP,
          JSON_CONSTANTS["NAME_KEY"]: state.name
        }
      )
    except (ConnectionError, Timeout, TooManyRedirects):
      state.remove_peer(original_source_ip)
  state.save_peers_to_file()
  return {}


@flask_app.route("/poke", methods=["POST"])
def poke():
  data: dict = request.get_json()
  source_ip = data[JSON_CONSTANTS["SOURCE_IP_KEY"]]
  print(f"poked by {source_ip}")
  source_name = data[JSON_CONSTANTS["NAME_KEY"]]
  user = User(source_name, source_ip)
  state.add_peer(source_ip, user)
  state.save_peers_to_file()
  return {}


def greet_outcome(state: State):
  out = [{
    JSON_CONSTANTS["IP_KEY"]: IP,
    JSON_CONSTANTS["NAME_KEY"]: state.name
  }]

  peer: User
  for ip, peer in state.get_peers_list():
    out.append({
      JSON_CONSTANTS["IP_KEY"]: ip,
      JSON_CONSTANTS["NAME_KEY"]: peer.name
    })

  return json.dumps({
    JSON_CONSTANTS["PEERS_KEY"]: out
  })
