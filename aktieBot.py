#
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies._strategy import _Strategy 
from lumibot.traders import Trader
from datetime import datetime

API_KEY = "PK68T85U8L3DVY4MDB1D"
API_SECRET = "TyxLmcfIeW929amzkDqmhmchh899s0Uy8cLKwrmr"
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY":API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

broker = Alpaca(ALPACA_CREDS)