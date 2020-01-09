from os import path
from datetime import datetime

from nicelka.engine.web_browser import WebBrowser


# TODO: write functional tests
# TODO: handle https://krkgw.arimr.gov.pl/

# TODO: move all files activities to separate class
# TODO: narrow all Exceptions into more specific classes
# TODO: add unit tests
# TODO: move whole package to separate project
# TODO: use REST API instead of Selenium?


class Searcher:
    _FILE_ENCODING = 'utf8'

    def __init__(self,
                 data_dir_path='data',
                 results_dir_path='results',
                 skip_indirect_matches=True,
                 skip_duplicates=True):
        self._data_dir_path = data_dir_path
        self._cities_file = self._assemble_data_file_path('cities.txt')
        self._keys_file = self._assemble_data_file_path('keys.txt')
        self._cities = self._get_cities()
        self._keys = self._get_keys()

        self._skip_indirect_matches = skip_indirect_matches
        self._skip_duplicates = skip_duplicates

        self._results = []
        self._results_count = 0
        self._results_dir_path = results_dir_path
        self._results_file_path = None

        self._engine = WebBrowser()

    def search(self):
        self._results_file_path = self._assemble_result_file_path()
        self._engine.start()

        for city in self._cities:
            self._add_city_header(city)

            for key in self._keys:
                result = []
                try:
                    result = self._engine.search(city, key)
                except Exception:
                    pass
                finally:
                    self._add_result(result, city, key)
                    self._save_results()

        self._add_results_count()
        self._save_results()

        self._engine.stop()

    def _assemble_data_file_path(self, file_name):
        return path.join(self._data_dir_path, file_name)

    def _get_cities(self):
        with open(self._cities_file, encoding=self._FILE_ENCODING) as file:
            return [city.strip() for city in file.readlines()]

    def _get_keys(self):
        with open(self._keys_file, encoding=self._FILE_ENCODING) as file:
            return [key.strip() for key in file.readlines()]

    def _assemble_result_file_path(self):
        return path.join(self._results_dir_path, '{}_raw.txt'.format(datetime.now()).replace(' ', '_').replace(':', '.'))

    def _add_city_header(self, city):
        self._results.append('=' * 70 + '\n')
        self._results.append(city + '\n\n')

    def _add_result(self, result, city, key):
        if result:
            self._results.append('#' + key + '\n\n')
            city_name = city.split(' ')[1]
            zip_code_prefix = city.split('-')[0] + '-'
            for item in result:
                if self._skip_indirect_matches and (city_name.lower() not in item.lower() or zip_code_prefix not in item.lower()):
                    continue
                if self._skip_duplicates and item + '\n' in self._results:
                    continue
                else:
                    self._results.append(item + '\n')
                    self._results_count += 1

    def _add_results_count(self):
        self._results.append('Liczba znalezionych adresow: {}'.format(self._results_count))

    def _save_results(self):
        try:
            with open(path.join(self._results_file_path), mode='w', encoding=self._FILE_ENCODING) as file:
                file.writelines(self._results)
        except Exception:
            pass
