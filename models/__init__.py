from sqlalchemy import Column, BigInteger, String, Float, Boolean, DateTime, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config.config import Config

Base = declarative_base()

class Trade(Base):
    __tablename__ = "trades"
    trade_id = Column(BigInteger, primary_key=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Float)
    buyer_is_maker = Column(Boolean)
    trade_time = Column(DateTime, index=True)

class Kline(Base):
    __tablename__ = "klines"
    symbol = Column(String)
    interval = Column(String)
    open_time = Column(DateTime)
    close_time = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    __table_args__ = (PrimaryKeyConstraint('symbol', 'interval', 'open_time'),)

class TechnicalIndicator(Base):
    __tablename__ = "technical_indicators"
    symbol = Column(String)
    interval = Column(String)
    timestamp = Column(DateTime)
    indicator_name = Column(String)
    indicator_value = Column(Float)
    __table_args__ = (PrimaryKeyConstraint('symbol', 'interval', 'timestamp', 'indicator_name'),)

# Initialize database
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)