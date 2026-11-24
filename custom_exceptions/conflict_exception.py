
class ConflictException(Exception):
    def __init__(self, message: str = 'resource already exists') -> None:
        super().__init__(message)