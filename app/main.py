from fastapi import FastAPI
from app.routes import user
from app.database.database import init_db
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI app
app = FastAPI()

# Initialize the database
try:
    init_db()
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

# Include routers from the routes module
# app.include_router(home.router)
app.include_router(user.router)