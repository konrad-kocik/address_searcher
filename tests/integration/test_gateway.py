import os

from nicelka.gateway.gateway import Gateway


def test_gateway_when_empty_lines_in_cities_skipped():
    gateway = Gateway(_get_data_dir_path(test_case='empty_lines_in_cities_skipped'))
    assert gateway.get_cities() == ['83-100 TCZEW', '83-110 KNYBAWA']


def test_gateway_when_empty_lines_in_keys_skipped():
    gateway = Gateway(_get_data_dir_path(test_case='empty_lines_in_keys_skipped'))
    assert gateway.get_keys() == ['Poczta', 'Emeryci', 'Emerytów']


def _get_data_dir_path(test_case):
    return os.path.join('data', 'gateway', test_case)
