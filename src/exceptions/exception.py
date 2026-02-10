"""All custom exceptions for the backoffice module."""


class TravelAgentError(Exception):
    """Base class for all custom exceptions in BackOffice."""

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        status_code: int | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code


