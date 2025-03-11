from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from services.historical import fetch_historical_klines
from services.indicators import compute_technical_indicators
from config.config import Config

def update_klines_and_indicators():
    for symbol in Config.SYMBOLS:
        for interval in Config.INTERVALS:
            fetch_historical_klines(symbol, interval, datetime.now() - timedelta(hours=1))
            compute_technical_indicators(symbol, interval)

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(update_klines_and_indicators, 'interval', minutes=5)
    scheduler.start()
    print("Scheduler started")
# The scheduler.py script is responsible for fetching historical klines and computing technical indicators for all symbols and intervals at a regular interval. It uses the apscheduler library to schedule a job that runs every 5 minutes. The update_klines_and_indicators function fetches historical klines for the past hour and computes technical indicators for each symbol and interval. The main block of the script starts the scheduler and prints a message to indicate that the scheduler has started.