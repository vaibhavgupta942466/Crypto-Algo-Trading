from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()