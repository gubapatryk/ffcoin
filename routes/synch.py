import json

import requests
from requests.exceptions import Timeout, TooManyRedirects, ConnectionError

from constants import HTTP_CONSTANTS, PORT, JSON_CONSTANTS, IP
from flask_app import flask_app
from flask import request, Response


@flask_app.route("/synch", methods=["POST"])
def synch():
  data = request.get_json()
  print(data)
  return {}
