from fastapi import HTTPException, status

class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = 400, detail: str = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail or message
        super().__init__(message)

class NotFoundError(AppException):
    """Resource not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)

class ValidationError(AppException):
    """Validation error"""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

class DuplicateError(AppException):
    """Duplicate record error"""
    def __init__(self, message: str = "Record already exists"):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)

class PermissionError(AppException):
    """Permission error"""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)

class AuthenticationError(AppException):
    """Authentication error"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)

class BusinessError(AppException):
    """Business logic error"""
    def __init__(self, message: str = "Business rule violation"):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)