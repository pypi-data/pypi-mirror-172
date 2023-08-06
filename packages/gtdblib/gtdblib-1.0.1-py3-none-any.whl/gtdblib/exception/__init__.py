class GtdbLibException(Exception):
    """Base exception for all gtdb-lib exceptions thrown in this project."""

    def __init__(self, message: str = ''):
        Exception.__init__(self, message)

