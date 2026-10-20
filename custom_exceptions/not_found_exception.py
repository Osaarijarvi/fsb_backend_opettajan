
class NotFoundException(Exception):
    def __init__(self, message: str = 'row not found in the database') -> None:
        super().__init__(message)