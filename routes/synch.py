import jsonpickle 
from flask import jsonify
from state import state

from flask_app import flask_app
from flask import request

from commands.blockchain import is_good_new_blockchain

@flask_app.route("/synch", methods=["POST"])
def synch():
  new_bc = jsonpickle.decode(request.get_json())
  if is_good_new_blockchain(state.blockchain.chain,new_bc):
    state.blockchain.chain = new_bc
    return "true"
  return "false"




@flask_app.route("/synch", methods=["GET"])
def send_chain():
  if state.hostile_mode:
    chain = state.blockchain.chain
    chain[len(chain) - 1].hash = "deadbeef"
    return jsonify({'json_data': jsonpickle.encode(chain)})
  else:
    return jsonify({'json_data': jsonpickle.encode(state.blockchain.chain)})