import os
import threading

from cli.cli_option import CLIOption
from cli.cli_definitions import cli_options, cli_map
from constants import IP, PORT
from flask_app import flask_app
from state import state

# don't remove these imports - users of toy languages don't get that decorators are not macros
# I'll add a ! each time I forget to register a route
# ! !
from routes.auth import *
from routes.greet import *
from routes.test_sign import *
from routes.synch import *

# blockchainery
from state.block import Block
from state.blockchain import Blockchain

if __name__ == "__main__":

  for cli_option in cli_options:
    print(f"{cli_option.code} - {cli_option.description}")

  
  def run_flask_app():
    flask_app.run(IP, port=os.getenv('PORT', PORT))

  flask_thread = threading.Thread(target=run_flask_app)
  flask_thread.start()
  
  while True:

    code: str = input("$ ").strip()
    cli_option: "CLIOption | None" = cli_map.get(code)

    if cli_option is None:
      print("Invalid option")
    else:
      cli_option.callback(state)
