class SignatureException(Exception):
  def __init__(self):
    super().__init__("Signature verification failure. See: https://tinyurl.com/49dx4c2r")
