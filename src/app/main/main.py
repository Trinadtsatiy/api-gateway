from typing import cast

from fastapi import FastAPI
from contextlib import asynccontextmanager
from faststream.asgi import AsgiFastStream
from starlette.types import ExceptionHandler

from src.app.infrastructure.brokers.nats_broker import broker
from src.app.presentation.api.services.auth.routers import router
from src.app.presentation.exception_handlers import validation_exc_handler
from src.app.domain.common.exceptions import DomainValidationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_faststream()
    yield


def init_faststream() -> AsgiFastStream:
    app = AsgiFastStream(broker, asyncapi_path='/docs')
    return app


def app_factory() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    app.add_exception_handler(
        DomainValidationError, cast(ExceptionHandler, validation_exc_handler)
    )
    return app
