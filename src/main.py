from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI


from src.exceptions import register_exception_handlers
from src.core import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifecycle events."""
    yield


# Create FastAPI app instance
app = FastAPI(
    title=settings["APP_NAME"],
    description=settings["APP_DESCRIPTION"],
    version=settings["APP_VERSION"],
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
    root_path="/backoffice",
)

register_exception_handlers(app)





if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings["SERVER_HOST"],
        port=settings["SERVER_PORT"],
        reload=settings["SERVER_DEBUG"],
    )
