"""Contains all custom exceptions for the interpreter."""

class UnmatchedScopeDesignator(Exception):
    """Raise when a scope designator like '[' or ']' is not properly matched."""