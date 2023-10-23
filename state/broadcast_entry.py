from datetime import datetime

from constants import TIMEZONE


class BroadcastEntry:

  def __init__(self, id: str, dt: "datetime | None" = None):
    self.id = id
    self.dt = dt if dt is not None else datetime.now(TIMEZONE)
