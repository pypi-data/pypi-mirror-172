from abc import ABCMeta

from algo_beast_core.algo_beast_broker_manager import algo_beast_broker_manager


class AlgoBeastStore(metaclass=ABCMeta):  
  __instance = None
  __strategy = None
  __data = []

  def __init__(self):
    if AlgoBeastStore.__instance:
      raise Exception("singleton can not be initiated more than one time")
    else:
      AlgoBeastStore.__instance = self

  @staticmethod
  def get_singleton():
    if AlgoBeastStore.__instance == None:
      AlgoBeastStore.__instance = AlgoBeastStore()

    return AlgoBeastStore.__instance

  def __register_strategy(self, strategy):
    self.__strategy = strategy

  def __register_session(self, session):
    self.__session = session

  def __set_broker(self):
    self.__broker = algo_beast_broker_manager.get_broker(self.__session)

  def __set_data(self, data):
    self.__data.append(data)

  def get_data(self):
    return self.__data

  def setup(self, strategy, session):
    self.__register_strategy(strategy)
    self.__register_session(session)
    self.__set_broker()
    self.__run()

  def __on_data(self, data):
    self.__set_data(data)
    self.__strategy.on_data(data)

  def __run(self):
    self.__strategy.initialize()
    self.__broker.fetch_data()
    self.__broker.subscribe(self.__on_data)

algo_beast_store = AlgoBeastStore.get_singleton()
