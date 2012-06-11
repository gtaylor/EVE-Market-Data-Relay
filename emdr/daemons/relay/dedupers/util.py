"""
Various utility functions that are common to all or many dedupers.
"""

def calc_hash_for_message(message):
    """
    Given an EMDR message string, calculate the hash.

    :param basestring message: A compressed or uncompressed EMDR message string.
    :rtype: str
    :returns: The hash to use for deduping.
    """
    # Use Python's naive 32bit integer hashing for now. It's fast and simple.
    return hash(message)