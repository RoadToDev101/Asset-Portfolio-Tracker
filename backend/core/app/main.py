from fastapi import FastAPI, Depends

# from supertokens_python import init, get_all_cors_headers
# from supertokens_python.framework.fastapi import get_middleware
# from supertokens_python.recipe.session import SessionContainer
# from supertokens_python.recipe.session.framework.fastapi import verify_session
# from supertokens_python.recipe.multitenancy.asyncio import list_all_tenants
# from app.supertokens_config import supertokens_config, app_info, framework, recipe_list
from app.utils.custom_exceptions import *
from app.routes import (
    user_route,
    authentication_route,
    portfolio_route,
    transaction_route,
)
from app.database.db_config import init_db, engine
from fastapi.middleware.cors import CORSMiddleware
from app.error_handling_middleware import exception_handling_middleware
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize SuperTokens
# init(
#     supertokens_config=supertokens_config,
#     app_info=app_info,
#     framework=framework,
#     recipe_list=recipe_list,
#     mode="asgi",
# )

# Create a FastAPI app
app = FastAPI(title="Portfolio Tracker API", version="0.0.1")
# app.add_middleware(get_middleware())

# Initialize the database
try:
    init_db(engine)
except Exception as e:
    print("Error initializing database: ", e)


# @app.get("/sessioninfo")
# async def secure_api(s: SessionContainer = Depends(verify_session())):
#     return {
#         "sessionHandle": s.get_handle(),
#         "userId": s.get_user_id(),
#         "accessTokenPayload": s.get_access_token_payload(),
#     }


# @app.get("/tenants")
# async def get_tenants():
#     tenantReponse = await list_all_tenants()

#     tenantsList = []

#     for tenant in tenantReponse.tenants:
#         tenantsList.append(tenant.to_json())

#     return {
#         "status": "OK",
#         "tenants": tenantsList,
#     }


# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_DOMAIN"), "http://localhost"],
    # allow_origins=[app_info.website_domain],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # allow_headers=["Content-Type"] + get_all_cors_headers(),
)

# Set up error handling middleware
app.middleware("http")(exception_handling_middleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Include routers from the routes module
app.include_router(user_route.router)
app.include_router(authentication_route.router)
app.include_router(portfolio_route.router)
app.include_router(transaction_route.router)
