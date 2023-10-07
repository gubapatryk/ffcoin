class CLIOption:

  def __init__(self, code, description, callback):
    self.code = code
    self.description = description
    self.callback = callback

  def call(self):
    self.callback()
