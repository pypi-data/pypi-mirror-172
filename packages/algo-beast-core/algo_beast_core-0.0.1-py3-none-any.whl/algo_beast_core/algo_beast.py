import sys
from abc import ABCMeta, abstractmethod

from core.algo_beast_store import algo_beast_store
from core.helpers.validate_session import validate_session


class AlgoBeast(metaclass=ABCMeta):
  data = algo_beast_store.get_data()

  def __init_subclass__(cls):
    session = validate_session(sys.argv)    
    algo_beast_strategy = cls()
    algo_beast_store.setup(algo_beast_strategy, session)

  @abstractmethod
  def initialize(self):
    pass
  
  @abstractmethod
  def on_data(self):
    pass

  @abstractmethod
  def set_starting_cash(self):
    pass

  @abstractmethod
  def set_start_date(self):
    pass
  
  @abstractmethod
  def set_end_date(self):
    pass
  
  @abstractmethod
  def set_warm_up(self):
    pass
