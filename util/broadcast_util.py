from random import randint
from time import time


def broadcast_id() -> str:
  return str(int(time())) + str(randint(0, 99999999))
