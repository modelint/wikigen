"""
exceptions.py – Model Execution exceptions
"""

class WGException(Exception):
    """ Top level Wiki generator exception """
    pass

class WGFileException(FileNotFoundError):
    pass
