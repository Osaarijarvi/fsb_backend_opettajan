
class UnauthorizedException(Exception):
    def __init__(self, message: str = 'unauthorized') -> None:
        super().__init__(message)
