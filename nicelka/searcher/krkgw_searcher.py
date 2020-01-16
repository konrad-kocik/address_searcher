from nicelka.engine.engine_factory import EngineFactory
from nicelka.reporter.reporter import Reporter
from nicelka.searcher.searcher import Searcher


class KrkgwSearcher(Searcher):
    def __init__(self,
                 data_dir_path='data',
                 results_dir_path='results',
                 skip_indirect_matches=True,
                 skip_duplicates=True):
        super(KrkgwSearcher, self).__init__(data_dir_path=data_dir_path,
                                            results_dir_path=results_dir_path,
                                            skip_indirect_matches=skip_indirect_matches,
                                            skip_duplicates=skip_duplicates)

        self._engine = EngineFactory.get_engine('krkgw_page')
        self._reporter = Reporter(results_dir_path, self.engine_name)

    def search(self):
        self._reporter.generate_new_report_file_path()
        self._engine.start()

        for city in self._cities:
            self._add_city_header(city)

            results = []
            try:
                results = self._engine.search(self._get_city_name(city))
            except Exception:
                pass
            finally:
                self._add_results(results, city)
                self._reporter.save_report(self._results)

        self._add_results_count()
        self._reporter.save_report(self._results)

        self._engine.stop()

    def _add_results(self, results, city):
        if results:
            zip_code_prefix = self._get_zip_code_prefix(city)
            city_name = self._get_city_name(city)

            if self._skip_indirect_matches:
                results = self._remove_indirect_matches(results, city_name, zip_code_prefix)

            if self._skip_duplicates:
                results = self._remove_duplicates(results)

            for result in results:
                self._results.append(result + '\n')
                self._results_count += 1
