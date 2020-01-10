import os

from pytest import fixture

import nicelka


@fixture
def test_cases():
    return ['no_result',
            'single_result',
            'single_result_indirect_match_by_city',
            'single_result_indirect_match_by_zip_code',
            'single_result_indirect_match_by_zip_code_tail']


@fixture
def create_results_dir(test_cases):
    for test_case in test_cases:
        result_dir_path = os.path.join('results', test_case)
        if not os.path.exists(result_dir_path):
            os.mkdir(result_dir_path)


@fixture
def remove_results_dir(test_cases, request):
    def teardown():
        for test_case in test_cases:
            result_dir_path = os.path.join('results', test_case)
            if os.path.exists(result_dir_path):
                os.system('cmd /k "rmdir /Q /S {}"'.format(result_dir_path))
    request.addfinalizer(teardown)


def test_searcher_when_no_result(create_results_dir, remove_results_dir):
    expected_result = \
        '======================================================================' + '\n' + \
        '24-200 BABIN' + '\n\n' + \
        'Liczba znalezionych adresow: 0'

    data_dir_path, results_dir_path = _get_io_dir_paths(test_case='no_result')
    searcher = _run_searcher(data_dir_path, results_dir_path)
    _assert_result_file_content_equals(expected_result, searcher.results_file_path)


def test_searcher_when_single_result(create_results_dir, remove_results_dir):
    expected_result = \
        '======================================================================' + '\n' + \
        '21-030 KONOPNICA' + '\n\n' + \
        '#Urząd' + '\n\n' + \
        'Urząd Gminy Konopnica' + '\n' + \
        'Kozubszczyzna 127a' + '\n' + \
        '21-030 Motycz' + '\n\n' + \
        'Liczba znalezionych adresow: 1'

    data_dir_path, results_dir_path = _get_io_dir_paths(test_case='single_result')
    searcher = _run_searcher(data_dir_path, results_dir_path)
    _assert_result_file_content_equals(expected_result, searcher.results_file_path)


def test_searcher_when_skipped_single_result_indirect_match_by_city(create_results_dir, remove_results_dir):
    expected_result = \
        '======================================================================' + '\n' + \
        '24-300 WOLA RUDZKA' + '\n\n' + \
        '#Przedszkole' + '\n\n' + \
        'Liczba znalezionych adresow: 0'

    data_dir_path, results_dir_path = _get_io_dir_paths(test_case='single_result_indirect_match_by_city')
    searcher = _run_searcher(data_dir_path, results_dir_path)
    _assert_result_file_content_equals(expected_result, searcher.results_file_path)


def test_searcher_when_skipped_single_result_indirect_match_by_zip_code(create_results_dir, remove_results_dir):
    expected_result = \
        '======================================================================' + '\n' + \
        '24-400 CUPLE' + '\n\n' + \
        '#Biblioteka' + '\n\n' + \
        'Liczba znalezionych adresow: 0'

    data_dir_path, results_dir_path = _get_io_dir_paths(test_case='single_result_indirect_match_by_zip_code')
    searcher = _run_searcher(data_dir_path, results_dir_path)
    _assert_result_file_content_equals(expected_result, searcher.results_file_path)


def test_searcher_when_not_skipped_single_result_indirect_match_by_zip_code_tail(create_results_dir):  # remove_results_dir
    expected_result = \
        '======================================================================' + '\n' + \
        '24-150 NAŁĘCZÓW' + '\n\n' + \
        '#Wydział' + '\n\n' + \
        'Urząd Miejski w Nałęczowie' + '\n' + \
        'Lipowa 3' + '\n' + \
        '24-140 Nałęczów' + '\n\n' + \
        'Liczba znalezionych adresow: 1'

    data_dir_path, results_dir_path = _get_io_dir_paths(test_case='single_result_indirect_match_by_zip_code_tail')
    searcher = _run_searcher(data_dir_path, results_dir_path)
    _assert_result_file_content_equals(expected_result, searcher.results_file_path)


def _get_io_dir_paths(test_case):
    return os.path.join('data', test_case), os.path.join('results', test_case)


def _run_searcher(data_dir_path, results_dir_path):
    searcher = nicelka.Searcher(data_dir_path, results_dir_path)
    searcher.search()
    return searcher


def _assert_result_file_content_equals(expected_result, results_file_path):
    with open(results_file_path, encoding='utf8') as file:
        assert file.read() == expected_result


# TODO: scenarios
'''
single result - allowed indirect match by city
single result - allowed indirect match by zip code
single result - allowed indirect match by zip code tail

single result - skipped duplicate
single result - allowed duplicate

single result twice

multiple results - three
multiple results - two
multiple results - one
multiple results - results not on top
multiple results skip all not direct match
multiple results skip one not direct match
multiple results allow one not direct match
multiple results skip all duplicated
multiple results skip one duplicated
multiple results allow one duplicated
multiple results twice
multiple results - zip code prefix matched
basic use case (mix of all scenarios)
'''
