from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///bot.db", echo=False)
Base = declarative_base()

_session = sessionmaker(bind=engine, future=True)

db_session = _session()
