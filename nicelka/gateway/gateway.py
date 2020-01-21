from os import path

from nicelka.logger.logger import Logger


class Gateway:
    _FILE_ENCODING = 'utf8'

    def __init__(self, data_dir_path):
        self._data_dir_path = data_dir_path
        self._cities_file_path = self._assemble_data_file_path('cities.txt')
        self._keys_file_path = self._assemble_data_file_path('keys.txt')
        self._black_list_filer_path = self._assemble_data_file_path('black_list.txt')

        Logger.info(self, 'Cities file path: {}'.format(self._cities_file_path))
        Logger.info(self, 'Keys file path: {}'.format(self._keys_file_path))

    def get_cities(self):
        Logger.info(self, 'Getting cities...')
        return self._get_items_from_file(self._cities_file_path)

    def get_keys(self):
        Logger.info(self, 'Getting keys...')
        return self._get_items_from_file(self._keys_file_path)

    def get_black_list(self):
        Logger.info(self, 'Getting black list...')
        return self._get_items_from_file(self._black_list_filer_path)

    def _assemble_data_file_path(self, file_name):
        return path.join(self._data_dir_path, file_name)

    def _get_items_from_file(self, file_path):
        with open(file_path, encoding=self._FILE_ENCODING) as file:
            return [item.strip() for item in file.readlines() if item.strip()]
