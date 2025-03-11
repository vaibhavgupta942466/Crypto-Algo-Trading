import pandas as pd
import ta
from database import get_session
from models import Kline, TechnicalIndicator
from config.config import Config

def compute_technical_indicators(symbol, interval):
    session = get_session()
    klines = session.query(Kline).filter_by(symbol=symbol, interval=interval).order_by(Kline.open_time.desc()).limit(100).all()
    df = pd.DataFrame([(k.open_time, k.open, k.high, k.low, k.close, k.volume) for k in klines],
                      columns=['open_time', 'open', 'high', 'low', 'close', 'volume'])
    df['close'] = df['close'].astype(float)

    # Compute indicators
    df['SMA_50'] = ta.trend.sma_indicator(df['close'], window=50)
    df['RSI'] = ta.momentum.rsi(df['close'], window=14)

    # Store indicators
    for _, row in df.iterrows():
        if pd.notna(row['SMA_50']):
            session.merge(TechnicalIndicator(
                symbol=symbol,
                interval=interval,
                timestamp=row['open_time'],
                indicator_name='SMA_50',
                indicator_value=row['SMA_50']
            ))
        if pd.notna(row['RSI']):
            session.merge(TechnicalIndicator(
                symbol=symbol,
                interval=interval,
                timestamp=row['open_time'],
                indicator_name='RSI',
                indicator_value=row['RSI']
            ))
    session.commit()
    session.close()