from pytest import fixture

from tests.integration.utilities.utilities import get_io_dir_paths, create_dir, remove_dir, run_krkgw_searcher, assert_report_file_content_equals


test_suite = 'krkgw_page'
test_cases = ['no_result',
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
              'multiple_results_on_multiple_pages_all_allowed',
              'multiple_results_on_multiple_pages_indirect_matches_skipped',
              'multiple_results_with_empty_details',
              'basic_use_cases'
              ]


@fixture(scope='module')
def create_reports_dirs():
    for test_case in test_cases:
        _, report_dir_path = get_io_dir_paths(test_suite, test_case)
        create_dir(report_dir_path)


@fixture(scope='module')
def remove_reports_dirs(request):
    def teardown():
        for test_case in test_cases:
            _, report_dir_path = get_io_dir_paths(test_suite, test_case)
            remove_dir(report_dir_path)
    request.addfinalizer(teardown)


def test_no_result(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '33-383 MUSZYNKA' + '\n\n' + \
        'Results found: 0'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='no_result')
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_no_result_twice(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '33-383 MUSZYNKA' + '\n\n' + \
        '======================================================================' + '\n' + \
        '33-322 JASIENNA' + '\n\n' + \
        'Results found: 0'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='no_result_twice')
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_single_result(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '21-075 ZEZULIN PIERWSZY' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Zezulin" w Zezulinie' + '\n' + \
        'Zezulin Pierwszy 22A' + '\n' + \
        '21-075 Zezulin Pierwszy' + '\n\n' + \
        'Results found: 1'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='single_result')
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_single_result_indirect_match_skipped(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '33-334 BOGUSZA' + '\n\n' + \
        'Results found: 0'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='single_result_indirect_match_skipped')
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_single_result_indirect_match_allowed(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '33-334 BOGUSZA' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Boguszach' + '\n' + \
        'Bogusze 45' + '\n' + \
        '16-100 Bogusze' + '\n\n' + \
        'Results found: 1'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='single_result_indirect_match_allowed')
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path, allow_indirect_matches=True)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_single_result_duplicate_skipped(create_reports_dirs, remove_reports_dirs):
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
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_single_result_duplicate_allowed(create_reports_dirs, remove_reports_dirs):
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
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path, allow_duplicates=True)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_single_result_twice(create_reports_dirs, remove_reports_dirs):
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
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_multiple_results(create_reports_dirs, remove_reports_dirs):
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
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_multiple_results_indirect_matches_skipped(create_reports_dirs, remove_reports_dirs):
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
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_multiple_results_indirect_matches_allowed(create_reports_dirs, remove_reports_dirs):
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
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path, allow_indirect_matches=True)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_multiple_results_duplicate_skipped(create_reports_dirs, remove_reports_dirs):
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
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_multiple_results_duplicate_allowed(create_reports_dirs, remove_reports_dirs):
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
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path, allow_duplicates=True)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_multiple_results_twice(create_reports_dirs, remove_reports_dirs):
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
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_multiple_results_on_multiple_pages_all_allowed(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '00-001 NOWA WIEŚ' + '\n\n' + \
        'Koło Gospodyń Wiejskich Nowa Wieś Niemczańska' + '\n' + \
        'Nowa Wieś Niemczańska 36 lok. 2' + '\n' + \
        '58-230 Nowa Wieś Niemczańska' + '\n\n' + \
        'Koło Gospodyń Wiejskich Nowowianki w Nowej Wsi Legnickiej' + '\n' + \
        'Nowa Wieś Legnicka 56' + '\n' + \
        '59-241 Nowa Wieś Legnicka' + '\n\n' + \
        'Koło Gospodyń Wiejskich POLANKI w Nowej Wsi Grodziskiej' + '\n' + \
        'Nowa Wieś Grodziska 54' + '\n' + \
        '59-524 Nowa Wieś Grodziska' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi "Ale Babki"' + '\n' + \
        'Nowa Wieś 63' + '\n' + \
        '87-602 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi' + '\n' + \
        'Nowa Wieś 80' + '\n' + \
        '88-324 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi' + '\n' + \
        'Nowa Wieś 76' + '\n' + \
        '21-107 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi' + '\n' + \
        'Nowa Wieś 20C' + '\n' + \
        '22-600 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi' + '\n' + \
        'Nowa Wieś 27' + '\n' + \
        '99-300 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich ,,Futuryści" w Nowej Wsi' + '\n' + \
        'Nowa Wieś 84' + '\n' + \
        '97-340 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich Nowa Wieś "Koniczynka"' + '\n' + \
        'Nowa Wieś 3' + '\n' + \
        '97-330 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich Szlachcianki' + '\n' + \
        'Nowa Wieś Szlachecka 1b' + '\n' + \
        '32-060 Nowa Wieś Szlachecka' + '\n\n' + \
        'Koło Gospodyń Wiejskich Nowa Wieś' + '\n' + \
        'Nowa Wieś 42' + '\n' + \
        '32-046 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi (gmina Łabowa)' + '\n' + \
        'Nowa Wieś 55' + '\n' + \
        '33-336 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi' + '\n' + \
        'Nowa Wieś 25' + '\n' + \
        '05-660 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Babeczki z pieprzem i solą' + '\n' + \
        'Nowa Wieś 52' + '\n' + \
        '26-900 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Nowalijki" w Nowej Wsi' + '\n' + \
        'ul. Reymonta 32 A' + '\n' + \
        '07-416 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Wschodniej' + '\n' + \
        'Nowa Wieś Wschodnia 32A' + '\n' + \
        '07-411 Nowa Wieś Wschodnia' + '\n\n' + \
        'Koło Gospodyń Wiejskich KAROLEWO-NOWA WIEŚ' + '\n' + \
        'Nowa Wieś 1' + '\n' + \
        '09-505 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Stokrotka"' + '\n' + \
        'Nowa Wieś 7B' + '\n' + \
        '09-440 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich Gospochy w Nowej Wsi' + '\n' + \
        'ul. Magnolii 7' + '\n' + \
        '05-806 Nowa Wieś' + '\n\n' + \
        'KOŁO GOSPODYŃ WIEJSKICH W NOWEJ WSI' + '\n' + \
        'ul. Wolności 37' + '\n' + \
        '08-300 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi' + '\n' + \
        'Nowa Wieś lok. 90' + '\n' + \
        '36-100 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi' + '\n' + \
        'Nowa Wieś 152 A' + '\n' + \
        '38-120 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich "Wespół w Zespół" w Nowej Wsi' + '\n' + \
        'Nowa Wieś 18F' + '\n' + \
        '16-402 Nowa Wieś' + '\n\n' + \
        'KOŁO GOSPODYŃ WIEJSKICH FIOŁKI W NOWEJ WSI' + '\n' + \
        'Nowa Wieś 4' + '\n' + \
        '77-320 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Przywidzkiej' + '\n' + \
        'ul. Szkolna 2' + '\n' + \
        '83-047 Nowa Wieś Przywidzka' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi' + '\n' + \
        'Nowa Wieś 41' + '\n' + \
        '42-110 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich Nowa Wieś' + '\n' + \
        'Nowa Wieś 100' + '\n' + \
        '28-362 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi' + '\n' + \
        'Nowa Wieś 25' + '\n' + \
        '27-640 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi „Nowalijki”' + '\n' + \
        'Nowa Wieś 9A' + '\n' + \
        '11-030 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Niechanowskiej "Storczyk"' + '\n' + \
        'Nowa Wieś Niechanowska 14' + '\n' + \
        '62-220 Nowa Wieś Niechanowska' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Książęcej' + '\n' + \
        'Nowa Wieś Książęca 35' + '\n' + \
        '63-640 Nowa Wieś Książęca' + '\n\n' + \
        'KOŁO GOSPODYŃ WIEJSKICH W NOWEJ WSI' + '\n' + \
        'Nowa Wieś ' + '\n' + \
        '63-708 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi' + '\n' + \
        'Nowa Wieś 19 lok. B7' + '\n' + \
        '63-308 Nowa Wieś' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Podgórnej' + '\n' + \
        'Nowa Wieś Podgórna 21 lok. 2' + '\n' + \
        '62-320 Nowa Wieś Podgórna' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Królewskiej' + '\n' + \
        'Nowa Wieś Królewska 22' + '\n' + \
        '62-300 Nowa Wieś Królewska' + '\n\n' + \
        'Results found: 36'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='multiple_results_on_multiple_pages_all_allowed')
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path, allow_indirect_matches=True, allow_duplicates=True)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_multiple_results_on_multiple_pages_indirect_matches_skipped(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '62-300 NOWA WIEŚ' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Niechanowskiej "Storczyk"' + '\n' + \
        'Nowa Wieś Niechanowska 14' + '\n' + \
        '62-220 Nowa Wieś Niechanowska' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Podgórnej' + '\n' + \
        'Nowa Wieś Podgórna 21 lok. 2' + '\n' + \
        '62-320 Nowa Wieś Podgórna' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Królewskiej' + '\n' + \
        'Nowa Wieś Królewska 22' + '\n' + \
        '62-300 Nowa Wieś Królewska' + '\n\n' + \
        'Results found: 3'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='multiple_results_on_multiple_pages_indirect_matches_skipped')
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_multiple_results_with_empty_details(create_reports_dirs, remove_reports_dirs):
    expected_report = \
        '======================================================================' + '\n' + \
        '89-200 TUR' + '\n\n' + \
        'Koło Gospodyń Wiejskich Centrum Kultury Ostrowite' + '\n' + \
        'ul. Szkolna 22' + '\n' + \
        '89-620 Ostrowite' + '\n\n' + \
        'Results found: 1'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='multiple_results_with_empty_details')
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)


def test_basic_use_cases(create_reports_dirs, remove_reports_dirs):
    """
    no_result
    single_result
    multiple_results
    no_result_twice
    single_result_indirect_match_skipped
    multiple_results_on_multiple_pages_indirect_matches_skipped
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
        '62-300 NOWA WIEŚ' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Niechanowskiej "Storczyk"' + '\n' + \
        'Nowa Wieś Niechanowska 14' + '\n' + \
        '62-220 Nowa Wieś Niechanowska' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Podgórnej' + '\n' + \
        'Nowa Wieś Podgórna 21 lok. 2' + '\n' + \
        '62-320 Nowa Wieś Podgórna' + '\n\n' + \
        'Koło Gospodyń Wiejskich w Nowej Wsi Królewskiej' + '\n' + \
        'Nowa Wieś Królewska 22' + '\n' + \
        '62-300 Nowa Wieś Królewska' + '\n\n' + \
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
        'Results found: 11'

    data_dir_path, report_dir_path = get_io_dir_paths(test_suite, test_case='basic_use_cases')
    searcher = run_krkgw_searcher(data_dir_path, report_dir_path)
    assert_report_file_content_equals(expected_report, searcher.report_file_path)
