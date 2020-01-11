from nicelka.engine.google_page import GooglePage
from nicelka.engine.krkgw_page import KrkgwPage


class EngineFactory:

    _ENGINE_TYPES = {'google_page': GooglePage,
                     'krkgw_page': KrkgwPage}

    @classmethod
    def get_engine(cls, engine_type):
        return cls._ENGINE_TYPES[engine_type]()
