from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from dotenv import load_dotenv
import os
from src.database.base import Base

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")

try:
    # Connect to the default 'postgres' database
    conn = psycopg2.connect(
        dbname="postgres",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST
    )
except psycopg2.OperationalError as e:
    print(f"Could not connect to the PostgreSQL server: {e}")
    exit(1)

conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor()
cur.execute("SELECT datname FROM pg_database;")
list_database = cur.fetchall()
if (POSTGRES_DB,) not in list_database:
    cur.execute(f"CREATE DATABASE {POSTGRES_DB};")
cur.close()
conn.close()

SQLALCHEMY_DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
except Exception as e:
    print(f"Could not create SQLAlchemy engine: {e}")
    exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Import all models here
    from src.models import user, portfolio, transaction

    Base.metadata.create_all(bind=engine)
