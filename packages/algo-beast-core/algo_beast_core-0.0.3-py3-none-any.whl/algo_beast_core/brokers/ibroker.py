from abc import ABC, abstractclassmethod


class IBroker(ABC):
  @property
  @abstractclassmethod
  def name(self):
    pass

  @property
  @abstractclassmethod
  def supported_modes(self):
    pass

  @abstractclassmethod
  def __init__(self, broker_config) -> None:
    pass
