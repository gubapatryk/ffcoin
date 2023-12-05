import json

from requests.exceptions import Timeout, TooManyRedirects, ConnectionError
from time import time
from constants import PORT, IP, HTTP_CONSTANTS, JSON_CONSTANTS
from random import randint
import requests

from state import State, User
from util.broadcast_util import broadcast_id
from util.signing import try_verify_response


def register(state: State):
  greet_peers(state)


# deprecated
def greet_peers(state: State):
  ip: str
  user: User
  for ip, user in state.peers.copy().items():
    if user.public_key is not None:
      try:
        # blocking
        out = requests.post(
          f"http://{ip}:{PORT}/greet",
          headers={
            HTTP_CONSTANTS["SOURCE_IP_HEADER"]: IP,
            HTTP_CONSTANTS["NAME_HEADER"]: state.name
          }
        )
        try_verify_response(state, ip, out)
        js_val = json.loads(out.text)
        user_response: list[dict] = js_val[JSON_CONSTANTS["PEERS_KEY"]]
        for user_dict in user_response:
          new_user_ip = user_dict[JSON_CONSTANTS["IP_KEY"]]
          new_user = User(user_dict[JSON_CONSTANTS["NAME_KEY"]], new_user_ip)
          state.add_peer(new_user_ip, new_user)
      except (ConnectionError, Timeout, TooManyRedirects):
        state.remove_peer(ip)
    else:
      print(f"No public key for {ip}, shaking hands is an option")


def broadcast(state: State):
  msg_id: str = broadcast_id()
  ip: str
  user: User
  for ip, user in state.peers.copy().items():
    if ip != IP:
      try:
        print(f"broadcast to {ip}")
        requests.post(
          f"http://{ip}:{PORT}/broadcast", json={
            JSON_CONSTANTS["BROADCAST_MESSAGE_ID"]: msg_id,
            JSON_CONSTANTS["SOURCE_IP_KEY"]: IP,
            JSON_CONSTANTS["NAME_KEY"]: state.name
          }
        )
        print("finished request")
      except (ConnectionError, Timeout, TooManyRedirects):
        state.remove_peer(ip)
  state.save_peers_to_file()
