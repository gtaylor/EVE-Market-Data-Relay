"""
Assorted utility functions for order and history serializing and
de-serializing.
"""
import dateutil.parser

def parse_iso8601_str(iso_str):
    """
    Given an ISO 8601 string, parse it and spit out a datetime.datetime
    instances.

    :param str iso_str: An ISO 8601 date string.
    :rtype: datetime.datetime
    """
    return dateutil.parser.parse(iso_str)

def _columns_to_kwargs(conversion_table, columns, row):
    """
    Given a list of column names, and a list of values (a row), return a dict
    of kwargs that may be used to instantiate a MarketHistoryEntry
    or MarketOrder object.

    :param dict conversion_table: The conversion table to use for mapping
        spec names to kwargs.
    :param list columns: A list of column names.
    :param list row: A list of values.
    """
    kwdict = {}

    counter = 0
    for column in columns:
        # Map the column name to the correct MarketHistoryEntry kwarg.
        kwarg_name = conversion_table[column]
        # Set the kwarg to the correct value from the row.
        kwdict[kwarg_name] = row[counter]
        counter += 1

    return kwdict