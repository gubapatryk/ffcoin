from cli.cli_option import CLIOption
from commands.registration import register
from commands.state import print_user_peers
from commands.wallet import set_up_keys, load_keys

cli_options = [
  CLIOption("1", "Create key pair", set_up_keys),
  CLIOption("2", "Load key pair", load_keys),
  CLIOption("3", "Broadcast greetings to known peers", register),
  CLIOption("4", "List peers", print_user_peers),
  CLIOption("exit", "Exit", lambda _: exit())
]

cli_map = {cli_option.code: cli_option for cli_option in cli_options}
