from contextlib import asynccontextmanager

from api.routes import api_router
from core.common.data.initial import load_initial_data
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from settings.app import app_settings
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


@asynccontextmanager
async def lifespan(_: FastAPI):
    await load_initial_data()
    yield


app = FastAPI(
    root_path="/api",
    title="AniCosmicBackend API",
    lifespan=lifespan,
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
    ],
)

# TODO: не выводить все ошибки в ответе
@app.exception_handler(Exception)
async def exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, (HTTPException, ValidationError)):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )
