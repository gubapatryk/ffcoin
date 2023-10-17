import json

from constants import JSON_CONSTANTS
from flask_app import flask_app
from flask import Response

from state import state
from util.signing import sign_response


@flask_app.route("/name")
def get_name():
  out = {
    JSON_CONSTANTS["NAME_KEY"]: state.name
  }
  out = json.dumps(out)
  response = Response(out)
  return sign_response(state, response)
