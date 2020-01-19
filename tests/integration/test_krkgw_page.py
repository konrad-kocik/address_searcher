import os

from pytest import fixture

from nicelka import KrkgwSearcher
from tests.integration.utilities.utilities import get_io_dir_paths, run_searcher, assert_report_file_content_equals


test_suite = 'krkgw_page'


@fixture(scope='module')
def test_cases():
    return ['no_result',
            'no_result_twice',
            'single_result',
            'single_result_indirect_match_skipped',
            'single_result_indirect_match_allowed',
            'single_result_duplicate_skipped',
            'single_result_duplicate_allowed',
            'single_result_twice',
            'multiple_results',
            'multiple_results_indirect_matches_skipped',
            'multiple_results_indirect_matches_allowed',
            'multiple_results_duplicate_skipped',
            'multiple_results_duplicate_allowed',
            'multiple_results_twice',
            'basic_use_cases'
            ]


@fixture(scope='module')
def create_reports_dirs(test_cases):
    for test_case in test_cases:
        _, report_dir_path = get_io_dir_paths(test_suite, test_case)
        if not os.path.exists(report_dir_path):
            os.mkdir(report_dir_path)


@fixture(scope='module')
def remove_reports_dirs(test_cases, request):
    def teardown():
        for test_case in test_cases:
            _, report_dir_path = get_io_dir_paths(test_suite, test_case)
            if os.path.exists(report_dir_path):
                os.system('cmd /k "rmdir /Q /S {}"'.format(report_dir_path))
    request.addfinalizer(teardown)


def test_searcher_when_no_result(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '33-383 MUSZYNKA' + '\n\n' + \
        'Results found: 0'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='no_result')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_no_result_twice(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '33-383 MUSZYNKA' + '\n\n' + \
        '======================================================================' + '\n' + \
        '33-322 JASIENNA' + '\n\n' + \
        'Results found: 0'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='no_result_twice')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_single_result(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '21-075 ZEZULIN PIERWSZY' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Zezulin" w Zezulinie' + '\n' + \
        'Zezulin Pierwszy 22A' + '\n' + \
        '21-075 Zezulin Pierwszy' + '\n\n' + \
        'Results found: 1'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='single_result')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_single_result_indirect_match_skipped(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '33-334 BOGUSZA' + '\n\n' + \
        'Results found: 0'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='single_result_indirect_match_skipped')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_single_result_indirect_match_allowed(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '33-334 BOGUSZA' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Boguszach' + '\n' + \
        'Bogusze 45' + '\n' + \
        '16-100 Bogusze' + '\n\n' + \
        'Results found: 1'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='single_result_indirect_match_allowed')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path, skip_indirect_matches=False)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_single_result_duplicate_skipped(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '21-075 ZEZULIN PIERWSZY' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Zezulin" w Zezulinie' + '\n' + \
        'Zezulin Pierwszy 22A' + '\n' + \
        '21-075 Zezulin Pierwszy' + '\n\n' + \
        '======================================================================' + '\n' + \
        '21-075 ZEZULIN PIERWSZY' + '\n\n' + \
        'Results found: 1'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='single_result_duplicate_skipped')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_single_result_duplicate_allowed(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '21-075 ZEZULIN PIERWSZY' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Zezulin" w Zezulinie' + '\n' + \
        'Zezulin Pierwszy 22A' + '\n' + \
        '21-075 Zezulin Pierwszy' + '\n\n' + \
        '======================================================================' + '\n' + \
        '21-075 ZEZULIN PIERWSZY' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Zezulin" w Zezulinie' + '\n' + \
        'Zezulin Pierwszy 22A' + '\n' + \
        '21-075 Zezulin Pierwszy' + '\n\n' + \
        'Results found: 2'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='single_result_duplicate_allowed')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path, skip_duplicates=False)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_single_result_twice(create_reports_dirs, remove_reports_dirs):
    expected_report = \
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
        'Results found: 2'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='single_result_twice')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_multiple_results(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '38-315 KUNKOWA' + '\n\n' + \
        'Koło Gospodyń Wiejskich i Gospodarzy w Kunkowej' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Kunkowej i Leszczynach' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        'Results found: 2'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='multiple_results')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_multiple_results_indirect_matches_skipped(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '33-393 MARCINKOWICE' + '\n\n' + \
        'KOŁO GOSPODYŃ WIEJSKICH W MARCINKOWICACH' + '\n' + \
        'Marcinkowice 124' + '\n' + \
        '33-393 Marcinkowice' + '\n\n' + \
        'KOŁO GOSPODYŃ WIEJSKICH W MARCINKOWICACH' + '\n' + \
        'Marcinkowice 104' + '\n' + \
        '33-393 Marcinkowice' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Marcinkowicanki"' + '\n' + \
        'Marcinkowice 47' + '\n' + \
        '33-273 Marcinkowice' + '\n\n' + \
        'Results found: 3'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='multiple_results_indirect_matches_skipped')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_multiple_results_indirect_matches_allowed(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '24-100 TOMASZÓW' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Tomaszowie' + '\n' + \
        'Tomaszów lok. 39' + '\n' + \
        '24-100 Tomaszów' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Tomaszowie' + '\n' + \
        'Tomaszów 44 "b"' + '\n' + \
        '26-505 Tomaszów' + '\n\n' + \
        'Results found: 2'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='multiple_results_indirect_matches_allowed')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path, skip_indirect_matches=False)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_multiple_results_duplicate_skipped(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '38-315 KUNKOWA' + '\n\n' + \
        'Koło Gospodyń Wiejskich i Gospodarzy w Kunkowej' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Kunkowej i Leszczynach' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        '======================================================================' + '\n' + \
        '38-315 KUNKOWA' + '\n\n' + \
        'Results found: 2'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='multiple_results_duplicate_skipped')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_multiple_results_duplicate_allowed(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '38-315 KUNKOWA' + '\n\n' + \
        'Koło Gospodyń Wiejskich i Gospodarzy w Kunkowej' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Kunkowej i Leszczynach' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        '======================================================================' + '\n' + \
        '38-315 KUNKOWA' + '\n\n' + \
        'Koło Gospodyń Wiejskich i Gospodarzy w Kunkowej' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Kunkowej i Leszczynach' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        'Results found: 4'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='multiple_results_duplicate_allowed')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path, skip_duplicates=False)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_when_multiple_results_twice(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '38-315 KUNKOWA' + '\n\n' + \
        'Koło Gospodyń Wiejskich i Gospodarzy w Kunkowej' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Kunkowej i Leszczynach' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        '======================================================================' + '\n' + \
        '33-393 MARCINKOWICE' + '\n\n' + \
        'KOŁO GOSPODYŃ WIEJSKICH W MARCINKOWICACH' + '\n' + \
        'Marcinkowice 124' + '\n' + \
        '33-393 Marcinkowice' + '\n\n' + \
        'KOŁO GOSPODYŃ WIEJSKICH W MARCINKOWICACH' + '\n' + \
        'Marcinkowice 104' + '\n' + \
        '33-393 Marcinkowice' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Marcinkowicanki"' + '\n' + \
        'Marcinkowice 47' + '\n' + \
        '33-273 Marcinkowice' + '\n\n' + \
        'Results found: 5'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='multiple_results_twice')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_searcher_basic_use_cases(create_reports_dirs, remove_reports_dirs):
    """
    no_result
    single_result
    multiple_results
    no_result_twice
    single_result_indirect_match_skipped
    single_result_duplicate_skipped
    multiple_results_twice
    single_result_twice
    """
    expected_report = \
        '======================================================================' + '\n' + \
        '33-383 MUSZYNKA' + '\n\n' + \
        '======================================================================' + '\n' + \
        '21-075 ZEZULIN PIERWSZY' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Zezulin" w Zezulinie' + '\n' + \
        'Zezulin Pierwszy 22A' + '\n' + \
        '21-075 Zezulin Pierwszy' + '\n\n' + \
        '======================================================================' + '\n' + \
        '38-315 KUNKOWA' + '\n\n' + \
        'Koło Gospodyń Wiejskich i Gospodarzy w Kunkowej' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Kunkowej i Leszczynach' + '\n' + \
        'Kunkowa 18' + '\n' + \
        '38-315 Kunkowa' + '\n\n' + \
        '======================================================================' + '\n' + \
        '33-383 MUSZYNKA' + '\n\n' + \
        '======================================================================' + '\n' + \
        '33-322 JASIENNA' + '\n\n' + \
        '======================================================================' + '\n' + \
        '33-334 BOGUSZA' + '\n\n' + \
        '======================================================================' + '\n' + \
        '21-075 ZEZULIN PIERWSZY' + '\n\n' + \
        '======================================================================' + '\n' + \
        '33-393 MARCINKOWICE' + '\n\n' + \
        'KOŁO GOSPODYŃ WIEJSKICH W MARCINKOWICACH' + '\n' + \
        'Marcinkowice 124' + '\n' + \
        '33-393 Marcinkowice' + '\n\n' + \
        'KOŁO GOSPODYŃ WIEJSKICH W MARCINKOWICACH' + '\n' + \
        'Marcinkowice 104' + '\n' + \
        '33-393 Marcinkowice' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Marcinkowicanki"' + '\n' + \
        'Marcinkowice 47' + '\n' + \
        '33-273 Marcinkowice' + '\n\n' + \
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
        'Results found: 8'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='basic_use_cases')
    searcher = run_searcher(KrkgwSearcher, data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)
