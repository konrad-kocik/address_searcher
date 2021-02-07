import os

from pytest import fixture

from nicelka.searcher.map_searcher import MapSearcher
from tests.integration.utilities.utilities import assert_report_file_content_equals, create_dir, remove_dir


@fixture
def data_dir_path():
    return os.path.join('data', 'map_page')


@fixture
def reports_dir_path():
    return os.path.join('reports', 'map_page', 'distances_from_one_main_city')


@fixture
def create_reports_dir(reports_dir_path):
    create_dir(reports_dir_path)


@fixture
def remove_reports_dir(reports_dir_path, request):
    def teardown():
        remove_dir(reports_dir_path)
    request.addfinalizer(teardown)


def test_distances_from_one_main_city(data_dir_path, reports_dir_path, create_reports_dir, remove_reports_dir):
    expected_report = \
        '======================================================================' + '\n' + \
        'Kraków' + '\n\n' + \
        '32-566 Alwernia: 39,3 km' + '\n' + \
        '34-120 Andrychów: 62,5 km' + '\n' + \
        '32-551 Babice: 46,9 km' + '\n' + \
        '34-116 Bachowice: 48,8 km' + '\n' + \
        '99-999 Dupowory: None' + '\n' + \
        '32-661 Bobrek: 61,2 km' + '\n'

    searcher = MapSearcher(main_city='Kraków', data_dir_path=data_dir_path, report_dir_path=reports_dir_path)
    searcher.search()
    assert_report_file_content_equals(expected_report, searcher.report_file_path)
