class Symbol:
  Nifty50 = "NSE:NIFTY50-INDEX"
  NiftyBank = "NSE:NIFTYBANK-INDEX"

class Timeframe:
  ONE_MINUTE = "1"

class Chart:
  def __init__(self, symbol: Symbol, timeframe: Timeframe):
    self.symbol = symbol
    self.timeframe = timeframe
    self.indicators = []
    self.filters = []

  def add_indicator(self, name, indicator, period):
    self.indicators.append(indicator)

  def add_filter(self, filter):
    self.indicators.append(filter)

