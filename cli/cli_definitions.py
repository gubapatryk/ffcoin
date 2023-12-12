from cli.cli_option import CLIOption
from commands.handshake import shake_hand, list_users_with_key
from commands.registration import register, broadcast
from commands.state_util import print_user_peers
from commands.test_verify import get_name_from_ip
from commands.transaction import commit_transaction
from commands.wallet import set_up_keys, load_keys
from commands.blockchain import print_blockchain, add_data_blockchain, force_update_blockchain, hostile_mode_switch, print_filtered

cli_options = [
  CLIOption("1", "Create key pair", set_up_keys),
  CLIOption("2", "Load key pair", load_keys),
  CLIOption("3d", "[deprecated] Broadcast greetings to known peers", register),
  CLIOption("3", "Broadcast greetings to known peers", broadcast),
  CLIOption("4", "Print state", print_user_peers),
  CLIOption("5", "Shake hand with user", shake_hand),
  CLIOption("6", "List users whose keys you have", list_users_with_key),
  CLIOption("7", "(test) Get username by ip and verify", get_name_from_ip),
  CLIOption("8", "Print blockchain", print_blockchain),
  CLIOption("9", "Add data to blockchain", add_data_blockchain),
  CLIOption("10", "Force update blockchain using other node", force_update_blockchain),
  CLIOption("11", "Switch hostile mode", hostile_mode_switch),
  CLIOption("12", "Transaction", commit_transaction),
  CLIOption("13", "Blockchain surfer", print_filtered),
  CLIOption("exit", "Exit", lambda _: exit())
]

cli_map: dict[str, CLIOption] = {cli_option.code: cli_option for cli_option in cli_options}
