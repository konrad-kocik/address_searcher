from datetime import datetime
from os import path
from contextlib import suppress

from xlwt import Workbook

from nicelka.logger.logger import Logger


class Reporter:
    _FILE_ENCODING = 'utf8'

    def __init__(self, report_dir_path, source):
        self._source = source
        self._report_dir_path = report_dir_path
        self._report_file_path = self._assemble_file_path('txt')
        self._excel_file_path = self._assemble_file_path('xls')

        Logger.info(self, 'Report file path: {}'.format(self._report_file_path))

    @property
    def report_file_path(self):
        return self._report_file_path

    def generate_new_report_file_path(self):
        self._report_file_path = self._assemble_file_path('txt')

    def save_report(self, results):
        with suppress(IOError):
            with open(self._report_file_path, mode='w', encoding=self._FILE_ENCODING) as file:
                file.writelines(results)

    def save_to_excel(self, results, title):
        workbook = Workbook()
        sheet = workbook.add_sheet(title)
        row_offset = 2

        sheet.write(0, 0, 'Kod pocztowy')
        sheet.write(0, 1, 'Miasto')
        sheet.write(0, 2, 'Odległość')

        for result_id, result in enumerate(results, start=1):
            if result_id in range(1, row_offset + 1) or not result:
                continue
            zip_code_and_city, distance = result.strip().split(': ')
            zip_code, city = zip_code_and_city.split(' ', maxsplit=1)
            sheet.write(result_id - row_offset, 0, zip_code)
            sheet.write(result_id - row_offset, 1, city)
            sheet.write(result_id - row_offset, 2, distance)

        workbook.save(self._excel_file_path)

    def _assemble_file_path(self, file_extension):
        return path.join(self._report_dir_path, '{}_{}.{}'.format(datetime.now(),
                                                                  self._source,
                                                                  file_extension).replace(' ', '_').replace(':', '.'))
