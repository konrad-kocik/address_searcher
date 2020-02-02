from nicelka.engine.engine_factory import EngineFactory
from nicelka.exceptions.exceptions import EngineException
from nicelka.logger.logger import Logger
from nicelka.reporter.reporter import Reporter
from nicelka.searcher.searcher import Searcher


class KrkgwSearcher(Searcher):
    def __init__(self,
                 data_dir_path='data',
                 report_dir_path='reports',
                 allow_indirect_matches=False,
                 allow_duplicates=False):
        super(KrkgwSearcher, self).__init__(data_dir_path=data_dir_path,
                                            allow_indirect_matches=allow_indirect_matches,
                                            allow_duplicates=allow_duplicates)

        self._engine = EngineFactory.get_engine('krkgw_page')
        self._reporter = Reporter(report_dir_path, self.engine_name)

    def search(self):
        Logger.info(self, 'Searching...')

        self._reporter.generate_new_report_file_path()
        self._engine.start()

        for city in self._cities:
            self._add_city_header(city)

            results = []
            try:
                results = self._engine.search(self._get_city_name(city))
            except EngineException as e:
                Logger.error(self, e)
            finally:
                self._add_results(results, city)
                self._reporter.save_report(self._results)

        self._add_results_count()
        self._reporter.save_report(self._results)

        self._engine.stop()

    def _add_results(self, results, city):
        if results:
            if not self._allow_indirect_matches:
                results = self._remove_indirect_matches(results, city)

            if not self._allow_duplicates:
                results = self._remove_duplicates(results)

            for result in results:
                self._results.append(result + '\n')
                self._results_count += 1
