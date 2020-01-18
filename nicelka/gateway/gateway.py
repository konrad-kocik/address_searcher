from os import path

from nicelka.logger.logger import Logger


class Gateway:
    _FILE_ENCODING = 'utf8'

    def __init__(self, data_dir_path):
        self._data_dir_path = data_dir_path
        self._cities_file_path = self._assemble_data_file_path('cities.txt')
        self._keys_file_path = self._assemble_data_file_path('keys.txt')

        Logger.info(self, 'Cities file path: {}'.format(self._cities_file_path))
        Logger.info(self, 'Keys file path: {}'.format(self._keys_file_path))

    def get_cities(self):
        Logger.info(self, 'Getting cities...')
        with open(self._cities_file_path, encoding=self._FILE_ENCODING) as file:
            return [city.strip() for city in file.readlines() if city.strip()]

    def get_keys(self):
        Logger.info(self, 'Getting keys...')
        with open(self._keys_file_path, encoding=self._FILE_ENCODING) as file:
            return [key.strip() for key in file.readlines() if key.strip()]

    def _assemble_data_file_path(self, file_name):
        return path.join(self._data_dir_path, file_name)
