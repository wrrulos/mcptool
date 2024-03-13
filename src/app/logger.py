import datetime
import logging
import os


class Logger:
    def __init__(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Create the log file
        log_file = f"logs/log_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.log"

        # Configure the logging
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def debug(message):
        logging.debug(message)

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def warning(message):
        logging.warning(message)

    @staticmethod
    def error(message):
        logging.error(message)

    @staticmethod
    def critical(message):
        logging.critical(message)
