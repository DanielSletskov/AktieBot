#aktiebot 
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.traders import Trader
from lumibot.strategies.strategy import Strategy
from datetime import datetime

API_KEY = "PK68T85U8L3DVY4MDB1D"
API_SECRET = "TyxLmcfIeW929amzkDqmhmchh899s0Uy8cLKwrmr"
BASE_URL = "https://paper-api.alpaca.markets/v2"

#Alpaca side which offers free api for stocks and news regarding them.
ALPACA_CREDS = {
    "API_KEY":API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

#Class for all trading strategy
class MLTrader(Strategy):
    def initializa(self, symbol:str="SPY"):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None

    def on_trading_iteration(self):
        if self.last_trade == None:
            order = self.create_order(
                self.symbol,
                10,
                "buy",
                type="market"
            )
            self.submit_order(order)
            self.last_trade = "buy"
            

#sets the limit for when we are testing 
start_date = datetime(2024,2,1)
end_date = datetime(2024,2,15)

broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlStrat', broker=broker,
                     parameters={"symbol":"SPY"})

strategy.backtest(
    YahooDataBacktesting, 
    start_date,
    end_date,
    parameters={"symbol":"SPY"}
)
