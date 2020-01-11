from os import path


class Gateway:
    _FILE_ENCODING = 'utf8'

    def __init__(self, data_dir_path):
        self._data_dir_path = data_dir_path
        self._cities_file_path = self._assemble_data_file_path('cities.txt')
        self._keys_file_path = self._assemble_data_file_path('keys.txt')

    def get_cities(self):
        with open(self._cities_file_path, encoding=self._FILE_ENCODING) as file:
            return [city.strip() for city in file.readlines()]

    def get_keys(self):
        with open(self._keys_file_path, encoding=self._FILE_ENCODING) as file:
            return [key.strip() for key in file.readlines()]

    def _assemble_data_file_path(self, file_name):
        return path.join(self._data_dir_path, file_name)
