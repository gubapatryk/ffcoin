import jsonpickle 
from flask import jsonify
from state import state
import requests
from requests.exceptions import Timeout, TooManyRedirects, ConnectionError

from constants import HTTP_CONSTANTS, PORT, JSON_CONSTANTS, IP
from flask_app import flask_app
from flask import request, Response


@flask_app.route("/synch", methods=["POST"])
def synch():
  state.blockchain.chain = jsonpickle.decode(request.get_json())
  print(request.get_json())
  print("lets goooo")
  print(state.blockchain)
  return {}

@flask_app.route("/synch", methods=["GET"])
def send_chain():
  return jsonify({'json_data': jsonpickle.encode(state.blockchain.chain)})