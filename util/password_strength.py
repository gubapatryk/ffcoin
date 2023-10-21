from constants import ENFORCE_PASSWORD_STRENGTH
import re

from util.exception.password_strength_exception import PasswordStrengthException


def try_password_strength(pswd: str) -> str:
  if ENFORCE_PASSWORD_STRENGTH:
    reasons: list = []
    if len(pswd) < 6:
      reasons.append("Password must contain at least 6 characters")
    if len(pswd) > 50:
      reasons.append("Password can't be longer than 50 characters")
    if not re.search(r"[!@#$%^&*_+=?\\/|:;,.<>\"'~{}]", pswd):
      reasons.append("Password must contain a special character")
    if not re.search(r"[0123456789]", pswd):
      reasons.append("Password must contain a number")
    if not re.search(r"[A-Z]", pswd):
      reasons.append("Password must contain a capital letter")
    if not re.search(r"[a-z]", pswd):
      reasons.append("Password must contain a lowercase letter")
    if len(reasons) is not 0:
      raise PasswordStrengthException(reasons)
  return pswd
