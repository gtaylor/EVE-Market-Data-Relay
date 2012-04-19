"""
Various utility functions for the included commands in the bin dir.
"""
import sys
from emdr.conf import default_settings

def set_logger_level(loglevel):
    """
    Given a log level from a --loglevel arg, set the root logger's level.

    :param str loglevel: One of DEBUG, INFO, WARNING, or ERROR.
    """
    loglevel = loglevel.upper()
    if loglevel not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
        print("Invalid log level. Must be one of: DEBUG, INFO, WARNING, ERROR")
        sys.exit(1)
    default_settings.LOGGING['loggers']['']['level'] = loglevel
    print("* Setting logging level to %s." % loglevel)