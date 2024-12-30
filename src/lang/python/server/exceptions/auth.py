from fastapi import status
from server.exceptions import ServerException

class InvalidCredentialsException(ServerException):
    """Raised when the credentials are invalid."""

class InvalidVerificationTokenException(ServerException):
    """Raised when the verification token is invalid."""

class InvalidPasswordResetTokenException(ServerException):
    """Raised when the password reset token is invalid."""

class TokenExpiredException(ServerException):
    """Raised when the token has expired."""

class EmailNotVerifiedException(ServerException):
    """Raised when the email is not verified."""

AUTH_EXCEPTIONS = {
    InvalidCredentialsException: {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": {
            "message": "Provided credentials are invalid",
            "error_code": "invalid_credentials",
        },
        "headers": {"WWW-Authenticate": "Bearer"},
    },
    InvalidVerificationTokenException: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": {
            "message":"Provided verification token is invalid",
            "error_code": "invalid_verification_token"
        }
    },
    InvalidPasswordResetTokenException: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": {
            "message":"Provided password reset token is invalid",
            "error_code": "invalid_password_reset_token"
        }
    },
    TokenExpiredException: {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": {
            "message": "Provided token has expired",
            "error_code": "token_expired",
        },
    },
    EmailNotVerifiedException: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": {
            "message": "Please verify your email address to activate your account.",
            "error_code": "email_not_verified",
        },
    },

}

