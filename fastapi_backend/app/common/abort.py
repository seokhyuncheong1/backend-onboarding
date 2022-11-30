from fastapi import status, HTTPException
from fastapi.responses import JSONResponse


def abort_exception(status_code: status, message: str):
    raise HTTPException(
        status_code=status_code,
        detail=message
    )


def abort_response(status_code: status, message: str):
    return JSONResponse(
        status_code=status_code,
        content={ "detail": message }
    )