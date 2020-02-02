class NicelkaException(Exception):
    pass


class EngineException(NicelkaException):
    pass


class WebPageException(EngineException):
    pass


class GooglePageException(WebPageException):
    pass


class GatewayException(NicelkaException):
    pass


class LoggerException(NicelkaException):
    pass


class ReporterException(NicelkaException):
    pass


class SearcherException(NicelkaException):
    pass
