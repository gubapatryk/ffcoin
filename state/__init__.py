from constants import PUBLIC_KEY_ENCODING, INITIAL_TRUSTED_IP, INITIAL_TRUSTED_NAME


class State:

  def __init__(self):
    self.name = None
    self.private_key = None
    self.public_key = None
    self.peers = {
      INITIAL_TRUSTED_NAME: INITIAL_TRUSTED_IP
    }

  def get_public_key_as_bytes(self):
    self.public_key.export_key(PUBLIC_KEY_ENCODING)


state = State()


def add_peer(state, peer, ip):
  state.peers[peer] = ip
