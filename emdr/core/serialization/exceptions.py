"""
Various parser-related exceptions.
"""

class InvalidMarketOrderDataError(Exception):
    """
    Raise this when invalid market order data is passed to a parser.
    """
    pass


class MessageParserError(Exception):
    """
    Raised when an error is encountered during the parsing of an incoming
    market data message.
    """
    pass