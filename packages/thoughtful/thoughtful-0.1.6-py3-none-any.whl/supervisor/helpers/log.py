import logging

try:
    from devtools import debug
except ImportError:
    pass
else:
    __builtins__['debug'] = debug

# Logging helper class for logging useful development data, must be manually
# enabled by adding @digitalworker(env=dev) or setting the global environment
# variable. See `supervisor.supervisor` for more information.
#
# Level    | When it's used
# DEBUG    | Detailed information, typically of interest only when diagnosing
#          | problems.
#
# INFO     | Confirmation that things are working as expected.
# WARNING  | An indication that something unexpected happened, or indicative
#          | of some problem in the near future (e.g. 'disk space low'). The
#          | software is still working as expected.
#
# ERROR    | Due to a more serious problem, the software has not been able to
#          | perform some function.
# CRITICAL | A serious error, indicating that the program itself may be unable
#          | to continue running.

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def create_logger():
    """
    Logger creation helper


    >>> logger = create_logger()
    >>> print(logger)
    """

    #create a logger object
    logger = logging.getLogger('reporter_debug_logger')
    logger.setLevel(logging.INFO)

    #create a file to store all the
    # logged exceptions
    logfile = logging.FileHandler('supervisor-debug.log')

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # / fmt = '%(levelname)s:%(message)s'
    formatter = logging.Formatter(fmt)

    logfile.setFormatter(formatter)
    logger.addHandler(logfile)

    return logger
