import requests
from Crypto.PublicKey import ECC

from constants import PORT, JSON_CONSTANTS, ECC_CURVE


def shake_hand(state):
  who = input("Provide username: ").strip()
  ip = state.peers.get(who)
  if ip is not None:
    shake_hand_by_ip(state, ip)
  else:
    print("Provided user does not exist, or is not discovered")


def shake_hand_by_ip(state, ip):
  out = requests.get(
    f"http://{ip}:{PORT}/public-key"
  )
  out = out.json()
  state.known_keys[out[JSON_CONSTANTS["NAME_KEY"]]] = ECC.import_key(
    out[JSON_CONSTANTS["PUBLIC_KEY_KEY"]], curve_name=ECC_CURVE
  )


def list_users_with_key(state):
  for user in state.known_keys:
    print(f" > {user}")
