from typing import List, Protocol


class Broker(Protocol):
  name: str
  supported_modes = List[str]

  def __init__(self, broker_config) -> None: ...

  def fetch_data(self): ...
  def subscribe(self, on_data): ...
