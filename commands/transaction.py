from constants import MINING_AWARD
from state import State
from state.block import Block
from state.transaction import Transaction


def commit_transaction(state: State):
  ip = input("Transaction to: ").strip()
  amount = float(input("Amount: ").strip())
  # verify if has enough funds
  transaction = Transaction(state.as_user().self_without_pk(), state.peers[ip].self_without_pk(), amount, MINING_AWARD)
  block = Block(transaction, state.get_last_hash())
  for ip, user in state.peers.copy().items():

