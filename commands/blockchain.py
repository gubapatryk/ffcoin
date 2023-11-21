from state import state

def print_blockchain(state):
    state.blockchain.display_blocks()

def add_data_blockchain(state):
    data = input("Provide data to save in blockchain: ").strip()
    state.blockchain.add_block_with_data(data)
