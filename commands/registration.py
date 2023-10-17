import json

from constants import INITIAL_TRUSTED_IP, PORT, IP, HTTP_CONSTANTS, JSON_CONSTANTS, INITIAL_TRUSTED_NAME
import requests

from util.signing import try_verify_response


def register(state):
  if len(state.peers) == 0:
    greet_peers(state, {
      INITIAL_TRUSTED_NAME: INITIAL_TRUSTED_IP
    })
  else:
    greet_peers(state, state.peers.copy())


def greet_peers(state, peers):
  for name, peer in peers.items():
    # blocking
    out = requests.post(
      f"http://{peer}:{PORT}/greet",
      headers={
        HTTP_CONSTANTS["SOURCE_IP_HEADER"]: IP,
        HTTP_CONSTANTS["NAME_HEADER"]: state.name
      }
    )
    try_verify_response(state, name, out)
    js_val = json.loads(out.text)
    state.peers.update(
      js_val[JSON_CONSTANTS["PEERS_KEY"]]
    )
