import os

from cli.cli_definitions import cli_options, cli_map
from constants import IP, PORT
from flask_app import flask_app
from state import state

if __name__ == "__main__":

  for cli_option in cli_options:
    print(f"{cli_option.code} - {cli_option.description}")

  flask_app.run(IP, port=os.getenv('PORT', PORT))

  while True:

    code = input("$ ").strip()
    cli_option = cli_map.get(code)

    if code is None:
      print("Invalid option")
    else:
      cli_option.callback(state)
