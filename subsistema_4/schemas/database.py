from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

username = 'root'
password = 'aos2023'
host = 'db-subsistema-4'
port = '3306'
database = 'aos2023'

DB_URL = f'mysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(DB_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
  Base.metadata.create_all(engine)

def get_db():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()