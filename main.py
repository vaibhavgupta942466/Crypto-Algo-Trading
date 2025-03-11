import threading
from services.historical import fetch_historical_trades, fetch_historical_klines
from services.websocket import start_websocket
from services.scheduler import update_klines_and_indicators, BlockingScheduler
from config.config import Config
from datetime import datetime

def run_historical_fetch():
    for symbol in Config.SYMBOLS:
        fetch_historical_trades(symbol)
        for interval in Config.INTERVALS:
            fetch_historical_klines(symbol, interval, datetime(2023, 1, 1))

def run_websocket():
    start_websocket()

if __name__ == "__main__":
    # Fetch historical data once
    run_historical_fetch()
    print("Fetched historical data")

    # Start WebSocket in a separate thread
    websocket_thread = threading.Thread(target=run_websocket)
    websocket_thread.start()
    print("Started WebSocket")

    # Start scheduler for periodic updates
    update_klines_and_indicators()  # Initial run
    scheduler = BlockingScheduler()
    scheduler.add_job(update_klines_and_indicators, 'interval', minutes=5)
    scheduler.start()
    print("Started scheduler")