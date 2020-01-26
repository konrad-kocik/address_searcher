import logging
import os
from datetime import datetime


class Logger:
    _FILE_ENCODING = 'utf8'
    _log_file_path = os.path.join('logs', '{}.log'.format(datetime.now())).replace(' ', '_').replace(':', '.')
    _logs = {}

    @classmethod
    def info(cls, caller, msg):
        caller_name = cls._get_name(caller)
        log = cls._get_log(caller_name)
        log.info(msg)

    @classmethod
    def error(cls, caller, exc, msg=''):
        caller_name = cls._get_name(caller)
        log = cls._get_log(caller_name)
        log.error(msg + ' ' + cls._get_name(exc) + ': ' + str(exc).strip())

    @classmethod
    def debug(cls, caller, msg):
        caller_name = cls._get_name(caller)
        log = cls._get_log(caller_name)
        log.debug(msg)

    @classmethod
    def _create_log(cls, name):
        file_handler = logging.FileHandler(cls._log_file_path, encoding=cls._FILE_ENCODING)
        formatter = logging.Formatter('%(asctime)s | %(levelname)-5s | %(name)-16s | %(message)s')
        file_handler.setFormatter(formatter)

        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)
        log.addHandler(file_handler)

        return log

    @classmethod
    def _get_log(cls, caller_name):
        if caller_name not in cls._logs:
            cls._logs[caller_name] = cls._create_log(caller_name)

        return cls._logs[caller_name]

    @classmethod
    def _get_name(cls, obj):
        return obj.__class__.__name__
