from datetime import datetime
from os import path
from contextlib import suppress

from nicelka.logger.logger import Logger


class Reporter:
    _FILE_ENCODING = 'utf8'

    def __init__(self, report_dir_path, source):
        self._source = source
        self._report_dir_path = report_dir_path
        self._report_file_path = self._assemble_report_file_path()

        Logger.info(self, 'Report file path: {}'.format(self._report_file_path))

    @property
    def report_file_path(self):
        return self._report_file_path

    def generate_new_report_file_path(self):
        self._report_file_path = self._assemble_report_file_path()

    def save_report(self, results):
        with suppress(IOError):
            with open(self._report_file_path, mode='w', encoding=self._FILE_ENCODING) as file:
                file.writelines(results)

    def _assemble_report_file_path(self):
        return path.join(self._report_dir_path, '{}_{}.txt'.format(datetime.now(), self._source).replace(' ', '_').replace(':', '.'))
