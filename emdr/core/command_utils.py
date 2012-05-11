"""
Various utility functions for the included commands in the bin dir.
"""
import sys
from emdr.conf import default_settings

def set_logger_level(loglevel):
    """
    Given a log level from a --loglevel arg, set the root logger's level.

    :param str loglevel: One of DEBUG, INFO, WARNING, or ERROR.
    :rtype: str
    :returns: The string representation of the log level being set.
    """
    loglevel = loglevel.upper()
    if loglevel not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
        print("Invalid log level. Must be one of: DEBUG, INFO, WARNING, ERROR")
        sys.exit(1)
    default_settings.LOGGING['loggers']['']['level'] = loglevel
    return loglevel

def print_cmd_header(cmd_name):
    """
    Prints a header for display during startup.

    :param str cmd_name: The name of the command's bin file.
    """
    print("=" * 80)
    header_str = "## %s ##" % cmd_name
    print(header_str.center(80))
    print("-" * 80)

def print_cmd_footer():
    """
    Matching footer to go at the end of the start-up sequence.
    """
    print("=" * 80)