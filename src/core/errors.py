class DomainError(Exception):
    """
    Error de negocio: reglas de dominio incumplidas.
    """
    pass


class ValidationError(DomainError):
    """
    Error específico de validación de datos de entrada.
    """
    pass
