from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from scheduler.main import app

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    """
    Custom exception handler for request validation errors.
    """
    # TODO
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )
