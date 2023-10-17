from cli.cli_option import CLIOption
from commands.handshake import shake_hand, list_users_with_key
from commands.registration import register
from commands.state import print_user_peers
from commands.test_sign import get_name_from_ip
from commands.wallet import set_up_keys, load_keys

cli_options = [
  CLIOption("1", "Create key pair", set_up_keys),
  CLIOption("2", "Load key pair", load_keys),
  CLIOption("3", "Broadcast greetings to known peers", register),
  CLIOption("4", "List peers", print_user_peers),
  CLIOption("5", "Shake hand with user", shake_hand),
  CLIOption("6", "List users whose keys you have", list_users_with_key),
  CLIOption("7", "(test) Get username by ip and verify", get_name_from_ip),
  CLIOption("exit", "Exit", lambda _: exit())
]

cli_map = {cli_option.code: cli_option for cli_option in cli_options}
