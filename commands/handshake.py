import requests
from Crypto.PublicKey import ECC

from constants import PORT, JSON_CONSTANTS, ECC_CURVE
from state import User, State


def shake_hand(state):
  who = input("Provide ip: ").strip()
  user: User = state.peers.get(who)
  if user is not None:
    shake_hand_by_ip(state, user)
  else:
    print("Provided user does not exist, or is not discovered")


def shake_hand_by_ip(state: State, user: User):
  out = requests.get(
    f"http://{user.ip}:{PORT}/public-key"
  )
  out = out.json()
  state.add_peer(
    user.ip,
    User(
      out[JSON_CONSTANTS["NAME_KEY"]],
      user.ip,
      ECC.import_key(
        out[JSON_CONSTANTS["PUBLIC_KEY_KEY"]], curve_name=ECC_CURVE
      )
    )
  )


def list_users_with_key(state: State):
  for ip, peer in state.peers.items():
    if peer.public_key is not None:
      print(f" > {ip} -> {peer.get_public_key_as_str()}")
