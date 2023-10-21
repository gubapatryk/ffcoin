class PasswordStrengthException(Exception):
  def __init__(self, reasons: list):
    self.reasons = reasons
    reasons_str = "\n".join(reasons)
    super().__init__(f"Provided password was to weak due to the following reasons:\n{reasons_str}")
