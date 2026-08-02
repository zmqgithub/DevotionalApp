class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundError(AppException):
    """Resource not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class ValidationError(AppException):
    """Validation error"""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=422)

class DuplicateError(AppException):
    """Duplicate record error"""
    def __init__(self, message: str = "Record already exists"):
        super().__init__(message, status_code=409)

class PermissionError(AppException):
    """Permission error"""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, status_code=403)

class AuthenticationError(AppException):
    """Authentication error"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)

class BusinessError(AppException):
    """Business logic error"""
    def __init__(self, message: str = "Business rule violation"):
        super().__init__(message, status_code=422)