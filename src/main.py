from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from database.database import Base, engine, SessionLocal
from schemas.user import User as UserSchema
from schemas.user import UserCreate
from controllers.user import UserController
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

# Create a FastAPI app
app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define the routes
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/{user_id}", response_model=UserSchema)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserController.get_user_by_id(db, user_id = user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users")
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    return UserController.create_user(db, user = user)

# Run the application
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)