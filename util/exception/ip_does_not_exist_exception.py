class IpDoesNotExistException(Exception):

  def __init__(self, ip: str):
    super().__init__(f"IP {ip} does not exist")
