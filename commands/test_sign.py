import json

import requests

from constants import PORT, JSON_CONSTANTS, HTTP_CONSTANTS
from util.signing import try_verify


def get_name_from_ip(state):
  print("WARNING: this command is completely useless")
  ip = input("Provide ip whose name to discover: ").strip()
  out = requests.get(
    f"http://{ip}:{PORT}/name"
  )
  js_val = json.loads(out.text)
  name = js_val[JSON_CONSTANTS["NAME_KEY"]]
  pub_key = state.known_keys[name]
  signature = out.headers[HTTP_CONSTANTS["SIGNATURE_HEADER"]]
  try_verify(pub_key, out.text, signature)
