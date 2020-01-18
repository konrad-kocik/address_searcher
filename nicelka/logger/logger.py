from datetime import datetime
import logging


class Logger:

    _log_file_path = 'logs\{}.log'.format(datetime.now()).replace(' ', '_').replace(':', '.')
    logging.basicConfig(filename=_log_file_path, level=logging.INFO)

    @staticmethod
    def info(caller, msg):
        logging.info(caller.__class__.__name__ + ': ' + msg)

    @staticmethod
    def error(caller, exc):
        logging.error(caller.__class__.__name__ + ': ' + exc.__class__.__name__ + ': ' + str(exc).strip())
