from typing import Protocol


class Session(Protocol):
  id: int
  user_id: int
  project_id: int
  mode: str
  broker_name: str
