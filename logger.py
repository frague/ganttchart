import sys
import logging
import logging.handlers

__author__ = 'Nick Bogdanov <nbogdanov@griddynamics.com>'

LOGGER_LEVEL = logging.DEBUG
LOGGER_FORMAT = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
LOGGER_HANDLER = logging.StreamHandler(sys.__stdout__)
LOGGER_HANDLER.setFormatter(LOGGER_FORMAT)

def make_custom_logger(name):
    """ Gets logger for specific script
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOGGER_LEVEL)
    logger.addHandler(LOGGER_HANDLER)
    return logger

