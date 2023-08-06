from abc import abstractmethod
from typing import Protocol


class Algorithm(Protocol):
  @abstractmethod
  def initialize(self): ...

  @abstractmethod
  def on_data(self): ...

  @abstractmethod
  def set_starting_cash(self): ...

  @abstractmethod
  def set_start_date(self): ...

  @abstractmethod
  def set_end_date(self): ...

  @abstractmethod
  def set_warm_up(self): ...
