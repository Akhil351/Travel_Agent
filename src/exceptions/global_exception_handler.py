"""Global exception handlers for the travel_agent module."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exception import TravelAgentError


def register_exception_handlers(app: FastAPI) -> None:
    """Register all Travel Agent exception handlers with FastAPI app."""

    @app.exception_handler(TravelAgentError)
    async def travel_agent_error_handler(
        _: Request, exc: TravelAgentError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code or 400,
            content={
                "success": False,
                "message": str(exc),
                "errorCode": exc.error_code,
                "item": [],
            },
        )
