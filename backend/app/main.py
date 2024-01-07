from fastapi import FastAPI
from app.utils.custom_exceptions import *
from app.routes import (
    user_route,
    authentication_route,
    portfolio_route,
    transaction_route,
)
from app.database.database import init_db, engine
from fastapi.middleware.cors import CORSMiddleware
from app.error_handling_middleware import exception_handling_middleware
from dotenv import load_dotenv


load_dotenv()

# Create a FastAPI app
app = FastAPI()

# Initialize the database
try:
    init_db(engine)
except Exception as e:
    print("Error initializing database: ", e)

# Set up CORS middleware
origins = ["http://localhost:3000", "localhost:3000", "http://localhost"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(exception_handling_middleware)

# Include routers from the routes module
app.include_router(user_route.router)
app.include_router(authentication_route.router)
app.include_router(portfolio_route.router)
app.include_router(transaction_route.router)
