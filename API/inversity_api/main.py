from contextlib import asynccontextmanager
from typing import AsyncIterator

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from inversity_api.config.app_config import get_app_settings
from inversity_api.data_structures.schemas.errors import ErrorDetail, ErrorResponse
from inversity_api.routers import health_checks as health_checks_router
from inversity_api.routers import lessons as lessons_router
from inversity_api.services.exceptions import ApiError

load_dotenv()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield


def get_openapi_docs_config(api_environment: str | None) -> tuple[str | None, str | None]:
    if api_environment != "dev":
        return None, None
    return "/docs", "/openapi.json"


settings = get_app_settings()
docs_url, openapi_url = get_openapi_docs_config(settings.api_environment)

app = FastAPI(
    title="PAIR Take-home API",
    docs_url=docs_url,
    openapi_url=openapi_url,
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ApiError)
async def handle_api_error(_: Request, exc: ApiError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorDetail(code=exc.code, message=exc.message)
        ).model_dump(),
    )


app.include_router(health_checks_router.router)
app.include_router(lessons_router.router)
