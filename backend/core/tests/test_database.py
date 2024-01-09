from app.database.database import (
    create_db_connection,
    create_database_if_not_exists,
    init_engine_and_session,
    init_db,
)
from dotenv import load_dotenv
import os
from app.dependencies import get_db
from app.main import app
from fastapi.testclient import TestClient

load_dotenv()

conn = create_db_connection(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    dbname="postgres",
)
create_database_if_not_exists(conn, f"{os.getenv('POSTGRES_DB')}_test")
engine, TestingSessionLocal = init_engine_and_session(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    db_name=f"{os.getenv('POSTGRES_DB')}_test",
)
init_db(engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        # Start a new transaction
        db.begin_nested()
        yield db
    except Exception as e:
        # In case of an exception, roll back the transaction
        db.rollback()
        raise e
    finally:
        # Always roll back the transaction after the test
        db.rollback()
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
