"""Server"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from vendor_manager_service.api.user_api import router as user_router
from app.database import SQLDAO
from app.custom_handler import (
    CustomException,
    custom_http_exception_handler,
)


# Context manager that will run before the server starts and after the server stops
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    app context manager
    """
    # Run things before the server starts
    sql_dao = SQLDAO()

    logger.debug("app started.")
    
    # test db connection if db session is async
    try:
        async with sql_dao.async_engine.connect() as conn:
            await conn.execute(select(1))
    except SQLAlchemyError as e:
        logger.error(f"database connection failed: {e}")
        raise e

    app.state.sql_dao = sql_dao

    # Important to yield after running things before the server starts
    yield  # run app

    # Run things before the server stops
    logger.debug("app stopped")


# Create the FastAPI app
app = FastAPI(
    title="User Manager Service",
    version="0.1.0",
    lifespan=lifespan,
    description="User Manager Service.",
    # default_response_class=ORJSONResponse,
)

# Custom


# Index route
# @app.get("/")
# async def index() -> ORJSONResponse:
#     return ORJSONResponse({"message": "SenseYoda Agent"})

# ================
# APP Router List

# http
app.include_router(user_router)

# ================
# custom handler
# app.add_exception_handler(CustomException, custom_http_exception_handler)
