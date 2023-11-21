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
    decision = input("Broadcast block?(type <yes> to send): ").strip()
    if decision == "yes":
        for ip, peer in state.peers.copy().items():
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
    for ip, peer in state.peers.copy().items():
            print(ip)
            try:
                res = requests.get(
                    f"http://{ip}:{PORT}/synch"
                )
                new_bc = jsonpickle.decode(res)
                print(new_bc)
                if is_good_new_blockchain(state.blockchain.chain,new_bc):
                    state.blockchain.chain = new_bc
                    break
            except:
                print(f'Route to {ip} not found')

def is_good_new_blockchain(org_bc,new_bc):
    for x in range(len(org_bc)-1,len(new_bc)):
        print("org hash")
        print(org_bc.hash)
        print("new hash")
        print(new_bc.hash)
    return True
