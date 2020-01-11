import os

from pytest import fixture

from nicelka import KrkgwSearcher


@fixture
def test_cases():
    return ['single_result',
            'no_result',
            'two_results',
            'multiple_results_indirect_matches',
            'single_result_twice']


@fixture
def create_results_dir(test_cases):
    for test_case in test_cases:
        _, result_dir_path = _get_io_dir_paths(test_case)
        if not os.path.exists(result_dir_path):
            os.mkdir(result_dir_path)


@fixture
def remove_results_dir(test_cases, request):
    def teardown():
        for test_case in test_cases:
            _, result_dir_path = _get_io_dir_paths(test_case)
            if os.path.exists(result_dir_path):
                os.system('cmd /k "rmdir /Q /S {}"'.format(result_dir_path))
    request.addfinalizer(teardown)


def test_searcher_when_no_result(create_results_dir, remove_results_dir):
    expected_result = \
        '======================================================================' + '\n' + \
        '33-383 MUSZYNKA' + '\n\n' + \
        'Liczba znalezionych adresow: 0'

    data_dir_path, results_dir_path = _get_io_dir_paths(test_case='no_result')
    searcher = _run_searcher(data_dir_path, results_dir_path)
    _assert_result_file_content_equals(expected_result, searcher.results_file_path)


def test_searcher_when_single_result(create_results_dir, remove_results_dir):
    expected_result = \
        '======================================================================' + '\n' + \
        '21-075 ZEZULIN PIERWSZY' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Zezulin" w Zezulinie' + '\n' + \
        'Zezulin Pierwszy 22A' + '\n' + \
        '21-075 Zezulin Pierwszy' + '\n\n' + \
        'Liczba znalezionych adresow: 1'

    data_dir_path, results_dir_path = _get_io_dir_paths(test_case='single_result')
    searcher = _run_searcher(data_dir_path, results_dir_path)
    _assert_result_file_content_equals(expected_result, searcher.results_file_path)


def test_searcher_when_allowed_multiple_results_indirect_matches(create_results_dir, remove_results_dir):
    expected_result = \
        '======================================================================' + '\n' + \
        '24-100 TOMASZÓW' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Tomaszowie' + '\n' + \
        'Tomaszów lok. 39' + '\n' + \
        '24-100 Tomaszów' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Tomaszowie' + '\n' + \
        'Tomaszów 44 "b"' + '\n' + \
        '26-505 Tomaszów' + '\n\n' + \
        'Liczba znalezionych adresow: 2'

    data_dir_path, results_dir_path = _get_io_dir_paths(test_case='multiple_results_indirect_matches')
    searcher = _run_searcher(data_dir_path, results_dir_path, skip_indirect_matches=False)
    _assert_result_file_content_equals(expected_result, searcher.results_file_path)


def test_searcher_when_single_result_twice(create_results_dir, remove_results_dir):
    expected_result = \
        '======================================================================' + '\n' + \
        '22-234 SĘKÓW' + '\n\n' + \
        'KOŁO GOSPODYŃ WIEJSKICH "BUBNOWSKIE BABY"' + '\n' + \
        'Sęków 15' + '\n' + \
        '22-234 Sęków' + '\n\n' + \
        '======================================================================' + '\n' + \
        '21-421 ZASTAWIE' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Zastawiu' + '\n' + \
        'Zastawie 47A' + '\n' + \
        '21-421 Zastawie' + '\n\n' + \
        'Liczba znalezionych adresow: 2'

    data_dir_path, results_dir_path = _get_io_dir_paths(test_case='single_result_twice')
    searcher = _run_searcher(data_dir_path, results_dir_path)
    _assert_result_file_content_equals(expected_result, searcher.results_file_path)


def _get_io_dir_paths(test_case):
    return os.path.join('data', 'krkgw_page', test_case), os.path.join('results', 'krkgw_page', test_case)


def _run_searcher(data_dir_path, results_dir_path, skip_indirect_matches=True):
    searcher = KrkgwSearcher(data_dir_path, results_dir_path, skip_indirect_matches=skip_indirect_matches)
    searcher.search()
    return searcher


def _assert_result_file_content_equals(expected_result, results_file_path):
    with open(results_file_path, encoding='utf8') as file:
        assert file.read() == expected_result
