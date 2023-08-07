from typing import Protocol


class Chart(Protocol):
  symbol: str
  timeframe: str
  candlestick: str
  indicators = []
  filters = []
  data = []

  def __init__(self, symbol: str, timeframe: str): ...

  def add_indicator(self, name, indicator): ...
  def add_filter(self, filter): ...

