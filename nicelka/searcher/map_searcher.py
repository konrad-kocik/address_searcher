from nicelka.engine.engine_factory import EngineFactory
from nicelka.exceptions.exceptions import EngineException
from nicelka.logger.logger import Logger
from nicelka.reporter.reporter import Reporter
from nicelka.searcher.searcher import Searcher


class MapSearcher(Searcher):
    def __init__(self,
                 main_city,
                 data_dir_path='data',
                 report_dir_path='reports'):
        super(MapSearcher, self).__init__(data_dir_path=data_dir_path)

        self._engine = EngineFactory.get_engine('map_page')
        self._main_city = main_city
        self._reporter = Reporter(report_dir_path, self.engine_name)

    def search(self):
        Logger.info(self, 'Searching...')

        self._reporter.generate_new_report_file_path()
        self._add_city_header(self._main_city)
        self._engine.start()

        for target_city in self._cities:
            results = None
            try:
                results = self._engine.search(self._main_city, target_city)
            except EngineException as e:
                Logger.error(self, e, self.search.__name__)
            finally:
                self._add_results(results, target_city)
                self._reporter.save_report(self._results)

        self._reporter.save_report(self._results)

        self._engine.stop()

    def _add_results(self, results, target_city):
        self._results.append(target_city + ' ' + str(results) + '\n')
        self._results_count += 1
