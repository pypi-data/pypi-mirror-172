from typing import Dict, List, Protocol, Type

from algo_beast_protocols.broker import Broker


class BrokerManager(Protocol):
  available_brokers: Dict[str, Type[Broker]]

  def __init__(self): ...

  def get_broker(self, session) -> Broker: ...
  def register(self, brokers: List[Broker]): ...
