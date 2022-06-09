from nicelka.engine.engine_factory import EngineFactory
from nicelka.exceptions.exceptions import EngineException
from nicelka.logger.logger import Logger
from nicelka.reporter.reporter import Reporter
from nicelka.searcher.searcher import Searcher


class GoogleSearcher(Searcher):
    def __init__(self,
                 data_dir_path='data',
                 report_dir_path='reports',
                 allow_indirect_matches=False,
                 allow_duplicates=False,
                 allow_blacklisted=False,
                 enable_engine_restart=False):
        super(GoogleSearcher, self).__init__(data_dir_path=data_dir_path,
                                             allow_indirect_matches=allow_indirect_matches,
                                             allow_duplicates=allow_duplicates)
        self._allow_blacklisted = allow_blacklisted
        Logger.info(self, 'Allowing blacklisted: {}'.format(self._allow_blacklisted))
        self._black_list = self._source.get_black_list()

        self._engine = EngineFactory.get_engine('google_page')
        self._engine_restart_frequency = 100 if enable_engine_restart else 0
        self._keys = self._source.get_keys()
        self._reporter = Reporter(report_dir_path, self.engine_name)

    def search(self):
        Logger.info(self, 'Searching...')

        self._reporter.generate_new_report_file_path()
        self._engine.start()
        search_count = 0

        for city in self._cities:
            search_count += 1
            self._add_city_header(city)

            for key in self._keys:
                results = []
                try:
                    results = self._engine.search(city, key)
                except EngineException as e:
                    Logger.error(self, e, self.search.__name__)
                finally:
                    self._add_results(results, city, key)
                    self._reporter.save_report(self._results)

            if self._engine_restart_frequency and search_count == self._engine_restart_frequency:
                search_count = 0
                Logger.debug(self, 'Restarting engine after {} searches...'.format(self._engine_restart_frequency))
                self._engine.restart()

        self._add_results_count()
        self._reporter.save_report(self._results)

        self._engine.stop()

    def _add_results(self, results, city, key):
        if results:
            if not self._allow_blacklisted:
                results = self._remove_blacklisted(results)

            if not self._allow_indirect_matches:
                results = self._remove_indirect_matches(results, city)

            if not self._allow_duplicates:
                results = self._remove_duplicates(results)

            if results:
                self._results.append('#' + key + '\n\n')

            for result in results:
                self._results.append(result + '\n')
                self._results_count += 1

    def _remove_blacklisted(self, results):
        return list(filter(self._is_not_blacklisted, results))

    def _is_not_blacklisted(self, result):
        return not any([black_list_item.lower() in result.lower() for black_list_item in self._black_list])
