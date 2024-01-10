import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=int(os.getenv("PORT")),
        reload=bool(os.getenv("ENV") == "development"),
    )
