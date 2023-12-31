from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.utils.custom_exceptions import *
from app.routes import (
    user_route,
    authentication_route,
    portfolio_route,
    transaction_route,
)
from app.database.database import init_db, engine
from fastapi.middleware.cors import CORSMiddleware
import traceback
from dotenv import load_dotenv
import os

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


# Handling unexpected errors
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        if os.getenv("ENV") == "development":
            print("Error in middleware: ", e)
            # For debugging/development purposes, you can log the full traceback
            # or send it in the response. BE CAREFUL with this in production.
            trace = traceback.format_exc()
            return JSONResponse(
                {
                    "detail": "Internal Server Error",
                    "error": str(e),
                    "trace": trace,  # Only include this in a non-production environment
                },
                status_code=500,
            )
        else:
            return JSONResponse({"detail": "Internal Server Error"}, status_code=500)


# Include routers from the routes module
app.include_router(user_route.router)
app.include_router(authentication_route.router)
app.include_router(portfolio_route.router)
app.include_router(transaction_route.router)
