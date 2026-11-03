
class BusinessRuleException(Exception):
    """Pyyntö oli muodoltaan kelvollinen, mutta operaatio ei ole sallittu sääntöjen takia."""

    def __init__(self, message: str = 'operation not allowed') -> None:
        super().__init__(message)