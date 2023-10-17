import json

from constants import JSON_CONSTANTS
from flask_app import flask_app
from flask import Response

from state import state
from util.signing import sign_response


@flask_app.route("/name")
def get_name():
  print("get name")
  out = {
    JSON_CONSTANTS["NAME_KEY"]: state.name
  }
  print(out)
  out = json.dumps(out)
  print(out)
  response = Response(out)
  print(response)
  return sign_response(state, response)
