from abc import abstractmethod

from nicelka.gateway.gateway import Gateway
from nicelka.logger.logger import Logger


class Searcher:
    _FILE_ENCODING = 'utf8'

    def __init__(self,
                 data_dir_path='data',
                 allow_indirect_matches=False,
                 allow_duplicates=False):
        self._engine = None
        self._source = Gateway(data_dir_path)
        self._cities = self._source.get_cities()

        self._allow_indirect_matches = allow_indirect_matches
        self._allow_duplicates = allow_duplicates

        Logger.info(self, 'Allowing indirect matches: {}'.format(self._allow_indirect_matches))
        Logger.info(self, 'Allowing duplicates: {}'.format(self._allow_duplicates))

        self._results = []
        self._results_count = 0
        self._reporter = None

    @property
    def engine_name(self):
        return None if self._engine is None else self._engine.name

    @property
    def report_file_path(self):
        return self._reporter.report_file_path

    @abstractmethod
    def search(self):
        self._raise_not_implemented_error('search')

    def _raise_not_implemented_error(self, method_name):
        raise NotImplementedError('{} class missing required implementation of method: {}'.format(self.__class__.__name__, method_name))

    def _add_city_header(self, city):
        self._results.append('=' * 70 + '\n')
        self._results.append(city + '\n\n')

    @staticmethod
    def _get_zip_code_prefix(city):
        return city.split('-')[0] + '-' if city[2] == '-' else None

    @staticmethod
    def _get_city_name(city):
        city_split = city.split(' ', maxsplit=1)
        return city_split[1] if len(city_split) >= 2 else city

    def _remove_indirect_matches(self, results, city):
        return [result for result in results if not self._is_indirect_match(result, city)]

    def _is_indirect_match(self, result, city):
        zip_code_prefix = self._get_zip_code_prefix(city)
        city_name = self._get_city_name(city)
        city_name_in_result = self._is_city_name_in_result(city_name, result)

        return city_name_in_result if zip_code_prefix is None else city_name_in_result or self._is_zip_code_prefix_in_result(zip_code_prefix, result)

    @staticmethod
    def _is_city_name_in_result(city_name, result):
        return city_name.lower() not in result.lower()

    @staticmethod
    def _is_zip_code_prefix_in_result(zip_code_prefix, result):
        return zip_code_prefix not in result

    def _remove_duplicates(self, results):
        return [result for result in results if not self._is_duplicate(result)]

    def _is_duplicate(self, result):
        return result.lower() + '\n' in list(map(str.lower, self._results))

    def _add_results(self, *args, **kwargs):
        self._raise_not_implemented_error('_add_results')

    def _add_results_count(self):
        self._results.append('Results found: {}'.format(self._results_count))
