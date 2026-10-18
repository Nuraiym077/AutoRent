from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.engine import create_engine


DB_URL = 'sqlite:///auto.db'
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass