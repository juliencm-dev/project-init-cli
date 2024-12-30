from typing import Any, Dict, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from server.exceptions.auth import *
from server.exceptions.user import *

class ServerException(HTTPException):
    """Base class for all server exceptions."""

def register_exceptions(app: FastAPI):
    _register_auth_exceptions(app)
    _register_user_exceptions(app)

def _register_auth_exceptions(app: FastAPI):
    for exc, config in AUTH_EXCEPTIONS.items():
        app.add_exception_handler(
            exc,
            _create_exception_handler(
                config["status_code"], 
                config["detail"],
                headers=config.get("headers")
            )
        )

def _register_user_exceptions(app: FastAPI):
    for exc, config in USER_EXCEPTIONS.items():
        app.add_exception_handler(
            exc,
            _create_exception_handler(
                config["status_code"], 
                config["detail"],
                headers=config.get("headers")
            )
        )

def _create_exception_handler(status_code: int, detail: Any, headers: Optional[Dict[str, str]] = None):
    async def _exception_handler(request: Request, exc: Exception):
        response =  JSONResponse(
            content=detail,
            status_code=status_code,
        )
        if headers:
            response.headers.update(headers)
        
        return response

    return _exception_handler

