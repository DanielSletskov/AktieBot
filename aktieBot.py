#aktiebot 
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.traders.trader import Trader
from lumibot.strategies.strategy import Strategy
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta


API_KEY = "PK68T85U8L3DVY4MDB1D"
API_SECRET = "TyxLmcfIeW929amzkDqmhmchh899s0Uy8cLKwrmr"
BASE_URL = "https://paper-api.alpaca.markets/v2"

#Alpaca side which offers free api for stocks and news regarding them.
ALPACA_CREDS = {
    "API_KEY":API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

#Class for all trading strategy Life cycle methods
class MLTrader(Strategy):
    def initialize(self, symbol:str="SPY", cash_at_risk:float=.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL,key_id=API_KEY,secret_key=API_SECRET)

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price)
        return cash, last_price, quantity

    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strfttime('%Y-%m-%d'), three_days_prior('%Y-%m-%d'
                                                             )

    def get_news(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, 
                                 start=three_days_prior , 
                                 end=today)
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        return news

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        
        if cash > last_price:
            if self.last_trade == None:
                news = self.get_news()
                print(news)
                order = self.create_order(
                    self.symbol,
                    10,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price*1.20,
                    stop_loss_price=last_price*.95
                )
                self.submit_order(order)
                self.last_trade = "buy"
            

#sets the limit for when we are testing 
start_date = datetime(2024,3,1)
end_date = datetime(2024,3,15)

broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat', broker=broker,
                     parameters={"symbol":"SPY", 
                                 "cash_at_risk":.5})

strategy.backtest(
    YahooDataBacktesting, 
    start_date,
    end_date,
    parameters={"symbol":"SPY",
                "cash_at_risk":.5}
)
