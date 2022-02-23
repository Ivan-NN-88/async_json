"""Logging settings."""

# Standard modules.
import os
import sys
import logging
import logging.handlers
# Local modules.
from settings import Paths


class LogSets:
    """
    Sets for logging.
    """
    # Create directory for logs.
    if not os.path.exists(Paths.LOG_PATH):
        os.mkdir(Paths.LOG_PATH)
    # Delete last log.
    if os.path.exists(Paths.LAST_LOG_FILE_PATH):
        os.remove(Paths.LAST_LOG_FILE_PATH)

    @staticmethod
    def set_1():
        """
        Set № 1 - with rotation of logs by day.
        """
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(lineno)4s %(funcName)-20s %(levelname)-7s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.handlers.TimedRotatingFileHandler(Paths.LOG_FILE_PATH, when='midnight'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.info('*' * 100)
        logging.info('Installed for logging set №1.')

    @staticmethod
    def set_2():
        """
        Set № 2 - 1 general log and 1 latest fresh log.
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)20s *** %(funcName)30s *** %(lineno)4s *** %(levelname)8s *** %(message)s',
            datefmt='%d.%m.%Y %H:%M:%S',
            handlers=[
                logging.handlers.RotatingFileHandler(Paths.LOG_FILE_PATH, maxBytes=int(1e+7), backupCount=1),
                logging.handlers.RotatingFileHandler(Paths.LAST_LOG_FILE_PATH),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.info('*' * 100)
        logging.info('Installed for logging set №2.')

