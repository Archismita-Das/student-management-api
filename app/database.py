from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="roshni@1206das",
    host="localhost",
    database="student_db"
)

engine = create_engine(url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()