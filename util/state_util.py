from random import randint


def parse_peer_list(l: list):
  for _ in range(10):
    i = randint(0, len(l) - 1)
    j = randint(0, len(l) - 1)
    piv = l[i]
    l[i] = l[j]
    l[j] = piv
  return l
