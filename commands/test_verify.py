import requests

from constants import PORT
from state import State
from util.signing import try_verify_response


def get_name_from_ip(state: State):
  print("WARNING: this command is completely useless")
  ip = input("Provide ip whose name to discover: ").strip()
  out = requests.get(
    f"http://{ip}:{PORT}/name"
  )
  try_verify_response(state, ip, out)
