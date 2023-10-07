import json

from constants import JSON_CONSTANTS
from flask_app import flask_app
from state import state
from util import b64


@flask_app.route("/public-key")
def get_public_key():
  pub_key = state.get_public_key_as_bytes()
  pub_str = b64.b64_encode_bytes(pub_key)
  return public_key_outcome(pub_str)


def public_key_outcome(b64str):
  return json.dumps({
    JSON_CONSTANTS["PUBLIC_KEY_KEY"]: b64str
  })
