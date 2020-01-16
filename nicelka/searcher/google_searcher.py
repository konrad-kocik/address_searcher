from nicelka.engine.engine_factory import EngineFactory
from nicelka.reporter.reporter import Reporter
from nicelka.searcher.searcher import Searcher


class GoogleSearcher(Searcher):
    def __init__(self,
                 data_dir_path='data',
                 results_dir_path='results',
                 skip_indirect_matches=True,
                 skip_duplicates=True):
        super(GoogleSearcher, self).__init__(data_dir_path=data_dir_path,
                                             results_dir_path=results_dir_path,
                                             skip_indirect_matches=skip_indirect_matches,
                                             skip_duplicates=skip_duplicates)

        self._engine = EngineFactory.get_engine('google_page')
        self._keys = self._source.get_keys()
        self._reporter = Reporter(results_dir_path, self.engine_name)

    def search(self):
        self._reporter.generate_new_report_file_path()
        self._engine.start()

        for city in self._cities:
            self._add_city_header(city)

            for key in self._keys:
                results = []
                try:
                    results = self._engine.search(city, key)
                except Exception:
                    pass
                finally:
                    self._add_results(results, city, key)
                    self._reporter.save_report(self._results)

        self._add_results_count()
        self._reporter.save_report(self._results)

        self._engine.stop()

    def _add_results(self, results, city, key):
        if results:
            self._results.append('#' + key + '\n\n')

            zip_code_prefix = self._get_zip_code_prefix(city)
            city_name = self._get_city_name(city)

            for result in results:
                if self._skip_indirect_matches and self._is_indirect_match(result, city_name, zip_code_prefix):
                    continue
                if self._skip_duplicates and self._is_duplicate(result):
                    continue
                else:
                    self._results.append(result + '\n')
                    self._results_count += 1
