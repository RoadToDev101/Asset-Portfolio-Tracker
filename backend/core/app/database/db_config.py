from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
import os
from dotenv import load_dotenv
from app.database.base import Base
import importlib


def load_db_environment_variables():
    load_dotenv()
    global POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")


def create_db_connection(user, password, host, port, dbname="postgres"):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Could not connect to the PostgreSQL server: {e}")
        exit(1)


def create_database_if_not_exists(connection, db_name):
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = connection.cursor()
    cur.execute("SELECT datname FROM pg_database;")
    list_database = cur.fetchall()
    if (db_name,) not in list_database:
        cur.execute(f"CREATE DATABASE {db_name};")
    cur.close()
    connection.close()


def init_engine_and_session(user, password, host, port, db_name):
    sqlalchemy_database_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    try:
        engine = create_engine(sqlalchemy_database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return engine, SessionLocal
    except Exception as e:
        print(f"Could not create SQLAlchemy engine: {e}")
        exit(1)


def init_db(engine):
    model_names = ["user_model", "portfolio_model", "transaction_model"]
    models = []

    for model_name in model_names:
        module = importlib.import_module(f"app.models.{model_name}")
        models.append(module)

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Could not create database tables: {e}")
        exit(1)


# Usage
load_db_environment_variables()
conn = create_db_connection(
    POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
)
create_database_if_not_exists(conn, POSTGRES_DB)
engine, SessionLocal = init_engine_and_session(
    POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
)
init_db(engine=engine)
