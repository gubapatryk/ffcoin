from state import state
import json 
import requests
from constants import PORT
import jsonpickle

def print_blockchain(state):
    state.blockchain.display_blocks()

def add_data_blockchain(state):
    data = input("Provide data to save in blockchain: ").strip()
    state.blockchain.add_block_with_data(data)
    for ip, peer in state.peers.copy().items():
        print(ip)
        try:
            requests.post(
                f"http://{ip}:{PORT}/synch", 
                json=jsonpickle.encode(state.blockchain.chain)
            )
        except:
            print(f'Route to {ip} not found')
    print("finished sending blockchain")
