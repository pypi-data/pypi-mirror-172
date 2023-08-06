from typing import Dict, List, Type

from algo_beast_core.brokers.algo_beast_broker import AlgoBeastBroker
from algo_beast_core.brokers.fyers_broker import FyersBroker
from algo_beast_core.brokers.ibroker import IBroker


class AlgoBeastBrokerManager:
  __instance = None

  available_brokers: Dict[str, Type[IBroker]] = {}

  def __init__(self):
    if AlgoBeastBrokerManager.__instance:
      raise Exception("singleton can not be initiated more than one time")
    else:
      AlgoBeastBrokerManager.__instance = self

  @staticmethod
  def get_singleton():
    if AlgoBeastBrokerManager.__instance == None:
      AlgoBeastBrokerManager.__instance = AlgoBeastBrokerManager()

    return AlgoBeastBrokerManager.__instance

  def get_broker(self, session) -> IBroker:
    broker_name, broker_config = session

    try:
      return self.available_brokers[broker_name](broker_config)
    except IndexError:
      raise Exception("Unknown broker")


  def register(self, brokers: List[IBroker]):
    for broker in brokers:
      self.available_brokers[broker.name] = broker

algo_beast_broker_manager = AlgoBeastBrokerManager.get_singleton()

# register brokers
algo_beast_broker_manager.register([
  AlgoBeastBroker,
  FyersBroker
])
