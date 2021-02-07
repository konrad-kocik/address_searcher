from nicelka.engine.google_page import GooglePage
from nicelka.engine.krkgw_page import KrkgwPage
from nicelka.engine.map_page import MapPage


class EngineFactory:

    _ENGINE_TYPES = {'google_page': GooglePage,
                     'krkgw_page': KrkgwPage,
                     'map_page': MapPage}

    @classmethod
    def get_engine(cls, engine_type):
        config = cls._get_config()
        args = (config['chrome_driver_exe_path'], ) if engine_type in ('google_page', 'krkgw_page', 'map_page') else ()
        return cls._ENGINE_TYPES[engine_type](*args)

    @classmethod
    def _get_config(cls):
        import nicelka.configs.golden
        return nicelka.configs.golden.config
