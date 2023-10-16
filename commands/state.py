def print_user_peers(state):
  for peer, ip in state.peers.items():
    print(f" > {peer} : {ip}")
