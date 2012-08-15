import sys
import logging
import logging.handlers

__author__ = 'Nick Bogdanov <nbogdanov@griddynamics.com>'

LOGGER_LEVEL = logging.INFO
LOGGER_FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOGGER_HANDLER = logging.StreamHandler(sys.__stdout__)
LOGGER_HANDLER.setFormatter(LOGGER_FORMAT)

def get_logger(name):
    """ Gets logger for specific script
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOGGER_LEVEL)
    logger.addHandler(LOGGER_HANDLER)
    return logger
