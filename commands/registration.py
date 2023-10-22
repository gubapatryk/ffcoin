import json

from constants import PORT, IP, HTTP_CONSTANTS, JSON_CONSTANTS
import requests

from state import State, User
from util.signing import try_verify_response


def register(state: State):
  greet_peers(state)


def greet_peers(state: State):
  ip: str
  user: User
  for ip, user in state.peers.copy():
    if user.public_key is not None:
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
    else:
      print(f"No public key for {ip}, shaking hands is an option")
