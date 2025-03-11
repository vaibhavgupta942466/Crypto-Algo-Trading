from binance import ThreadedWebsocketManager
from binance.client import Client
from twisted.internet import reactor
from database import get_session
from models import Trade
from config.config import Config
from datetime import datetime

client = Client(Config.BINANCE_API_KEY, Config.BINANCE_API_SECRET)

def process_message(msg):
    print(msg)
    trade = msg['data']
    session = get_session()
    session.merge(Trade(
        trade_id=int(trade['t']),
        symbol=trade['s'],
        price=float(trade['p']),
        quantity=float(trade['q']),
        buyer_is_maker=trade['m'],
        trade_time=datetime.utcfromtimestamp(trade['T'] / 1000.0)
    ))
    session.commit()
    session.close()

def start_websocket():
    bm = ThreadedWebsocketManager(client)
    bm.start_trade_socket(symbol=Config.SYMBOLS[0], callback=process_message)
    bm.start()

if __name__ == "__main__":
    start_websocket()
    reactor.run()