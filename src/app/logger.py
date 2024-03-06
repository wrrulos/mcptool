import datetime
import logging
import os


class Logger:
    def __init__(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Obtener la fecha y hora actual para nombrar el archivo de log
        current_datetime = datetime.datetime.now()
        log_file = f"logs/log_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.log"

        # Configurar el registro en un archivo
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def debug(self, message):
        logging.debug(message)

    def info(self, message):
        logging.info(message)

    def warning(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)

    def critical(self, message):
        logging.critical(message)
