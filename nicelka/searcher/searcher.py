from abc import abstractmethod

from nicelka.gateway.gateway import Gateway
from nicelka.reporter.reporter import Reporter

# TODO: fix bug in google_page when multiple results are not on top and google_page should return more then max 3 results
# TODO: write integration tests
# TODO: handle multiple result pages in KrkgwPage
# TODO: add logger
# TODO: narrow all Exceptions into more specific classes (report exceptions into logger)
# TODO: add progress bar
# TODO: refactor integration tests
# TODO: add unit tests
# TODO: store results in custom classes
# TODO: save result count every time when saving results
# TODO: use REST API instead of Selenium
# TODO: add AI to evaluate results found
# TODO: add docs, type hints etc.


class Searcher:
    _FILE_ENCODING = 'utf8'

    def __init__(self,
                 data_dir_path='data',
                 results_dir_path='results',
                 skip_indirect_matches=True,
                 skip_duplicates=True):
        self._engine = None
        self._source = Gateway(data_dir_path)
        self._cities = self._source.get_cities()

        self._skip_indirect_matches = skip_indirect_matches
        self._skip_duplicates = skip_duplicates

        self._results = []
        self._results_count = 0
        self._reporter = Reporter(results_dir_path, self.engine_name)

    @property
    def engine_name(self):
        return None if self._engine is None else self._engine.name

    @property
    def results_file_path(self):
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

    def _remove_indirect_matches(self, results, city_name, zip_code_prefix):
        return [result for result in results if not self._is_indirect_match(result, city_name, zip_code_prefix)]

    def _is_indirect_match(self, result, city_name, zip_code_prefix):
        city_name_in_result = self._is_city_name_in_result(city_name, result)
        return city_name_in_result if zip_code_prefix is None else city_name_in_result or self._is_zip_code_prefix_in_result(zip_code_prefix, result)

    @staticmethod
    def _is_city_name_in_result(city_name, result):
        return city_name.lower() not in result.lower()

    @staticmethod
    def _is_zip_code_prefix_in_result(zip_code_prefix, result):
        return zip_code_prefix not in result.lower()

    def _remove_duplicates(self, results):
        return [result for result in results if not self._is_duplicate(result)]

    def _is_duplicate(self, result):
        return result + '\n' in self._results

    def _add_results(self, *args, **kwargs):
        self._raise_not_implemented_error('_add_results')

    def _add_results_count(self):
        self._results.append('Liczba znalezionych adresow: {}'.format(self._results_count))
