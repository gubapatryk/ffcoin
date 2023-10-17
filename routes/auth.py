import json

from constants import JSON_CONSTANTS
from flask_app import flask_app
from state import state
from util import b64


@flask_app.route("/public-key")
def get_public_key():
  pub_key = state.get_public_key_as_str()
  print("####")
  print(pub_key)
  return public_key_outcome(pub_key)


def public_key_outcome(b64str):
  return json.dumps({
    JSON_CONSTANTS["PUBLIC_KEY_KEY"]: b64str,
    JSON_CONSTANTS["NAME_KEY"]: state.name
  })
