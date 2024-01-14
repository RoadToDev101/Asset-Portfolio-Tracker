from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
import os


async def exception_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        if os.getenv("ENV") == "development":
            print("Error in middleware: ", e)
            trace = traceback.format_exc()
            return JSONResponse(
                {
                    "detail": "Internal Server Error",
                    "error": str(e),
                    "trace": trace,
                },
                status_code=500,
            )
        else:
            return JSONResponse({"detail": "Internal Server Error"}, status_code=500)
