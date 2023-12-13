from state import state, Balance
import json
import requests
from constants import PORT, IP
import jsonpickle


def print_blockchain(state):
  state.blockchain.display_blocks()


def print_filtered(state):
  state.blockchain.print_filtered()


def add_data_blockchain(state):
  data = input("Provide data to save in blockchain: ").strip()
  state.blockchain.add_block_with_data(data)
  decision = input("Broadcast block?(type <yes> to send): ").strip()
  if decision == "yes":
    for ip, peer in state.get_peers_list():
      print(ip)
      try:
        print(jsonpickle.encode(state.blockchain.chain))
        requests.post(
          f"http://{ip}:{PORT}/synch",
          json=jsonpickle.encode(state.blockchain.chain)
        )
      except:
        print(f'Route to {ip} not found')
    print("finished sending blockchain")


def force_update_blockchain(state):
  for ip, peer in state.get_peers_list():
    if ip != IP:
      try:
        res = requests.get(
          f"http://{ip}:{PORT}/synch"
        )
        print(res.json()['json_data'])
        new_bc = jsonpickle.decode(res.json()['json_data'])

        if is_good_new_blockchain(state.blockchain.chain, new_bc):
          Balance(new_bc)
          print("zaktualizowano blockchain")
          state.blockchain.chain = new_bc
          break
      except Exception as e:
        print(e)
        print(f'Route to {ip} not found')


# Sprawdzanie czy nowy blockchain jest poprawny wzgledem dotychczasowych blokow
def is_good_new_blockchain(org_bc, new_bc):
  if len(org_bc) > len(new_bc):
    shrt_len = len(new_bc)
  else:
    shrt_len = len(org_bc)
  if len(org_bc) > 1:
    for x in range(1, shrt_len):
      if org_bc[x - 1].hash != new_bc[x - 1].hash:
        return False
      print("ok policz hasze")
      if new_bc[x - 1].calculate_hash() != new_bc[x - 1].hash:
        return False
  for x in range(shrt_len - 1, len(new_bc)):
    if x - 1 > 1:
      if new_bc[x - 2].calculate_hash() != new_bc[x - 1].previous_hash:
        return False
    if new_bc[x - 1].calculate_hash() != new_bc[x - 1].hash:
      return False
  return True


def hostile_mode_switch(state):
  print("Tryb falszowania blockchainu:")
  state.hostile_mode = not state.hostile_mode
  print(state.hostile_mode)
  return
