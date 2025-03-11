from binance.client import Client
from datetime import datetime
import time
from database import get_session
from models import Trade, Kline
from config.config import Config

client = Client(Config.BINANCE_API_KEY, Config.BINANCE_API_SECRET)

def fetch_historical_trades(symbol, limit=1000):
    session = get_session()
    latest_id = session.query(Trade.trade_id).filter_by(symbol=symbol).order_by(Trade.trade_id.desc()).first()
    start_id = latest_id[0] + 1 if latest_id else None
    while True:
        print(f"Fetching trades for {symbol} starting from {start_id}")
        trades = client.get_historical_trades(symbol=symbol, limit=limit, fromId=start_id)
        with open(f"logs/{symbol}_historical_trades.txt", "a") as f:
            f.write(f"{trades}\n")
        if not trades:
            break
        for trade in trades:
            session.merge(Trade(
                trade_id=int(trade['id']),
                symbol=symbol,
                price=float(trade['price']),
                quantity=float(trade['qty']),
                buyer_is_maker=trade['isBuyerMaker'],
                trade_time=datetime.utcfromtimestamp(trade['time'] / 1000.0)
            ))
        session.commit()
        if len(trades) < limit:
            break
        start_id = trades[-1]['id'] + 1
        time.sleep(0.1)

def fetch_historical_klines(symbol, interval, start_date):
    session = get_session()
    klines = client.get_historical_klines(symbol, interval, start_date.strftime("%d %b, %Y"))
    for kline in klines:
        session.merge(Kline(
            symbol=symbol,
            interval=interval,
            open_time=datetime.utcfromtimestamp(kline[0] / 1000.0),
            close_time=datetime.utcfromtimestamp(kline[6] / 1000.0),
            open=float(kline[1]),
            high=float(kline[2]),
            low=float(kline[3]),
            close=float(kline[4]),
            volume=float(kline[5])
        ))
    session.commit()
    session.close()