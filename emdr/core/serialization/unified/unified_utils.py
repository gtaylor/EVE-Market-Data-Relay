"""
Assorted utility functions for order and history serializing and
de-serializing.
"""
from emdr.core.serialization.common_utils import UTC_TZINFO

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

def gen_iso_datetime_str(dtime):
    """
    Convenience function for dumping a properly formatted ISO datetime
    string. Unified format requires an explicit timezone offset, and no
    microseconds, so take care of both of those.

    :param datetime.datetime dtime: The datetime to generate the ISO datetime
        string from.
    :rtype: str
    :returns: An ISO/Unified Uploader formatted datetime string.
    """
    return dtime.replace(microsecond=0, tzinfo=UTC_TZINFO).isoformat()