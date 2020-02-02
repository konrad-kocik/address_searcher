import os

from nicelka import GoogleSearcher, KrkgwSearcher


def get_io_dir_paths(test_suite, test_case):
    return os.path.join('data', test_suite, test_case), os.path.join('reports', test_suite, test_case)


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def remove_dir(dir_path):
    if os.path.exists(dir_path):
        os.system('cmd /k "rmdir /Q /S {}"'.format(dir_path))


def run_google_searcher(data_dir_path, report_file_path, allow_indirect_matches=False, allow_duplicates=False, allow_blacklisted=False):
    searcher = GoogleSearcher(data_dir_path, report_file_path,
                              allow_indirect_matches=allow_indirect_matches,
                              allow_duplicates=allow_duplicates,
                              allow_blacklisted=allow_blacklisted)
    searcher.search()
    return searcher


def run_krkgw_searcher(data_dir_path, report_file_path, allow_indirect_matches=False, allow_duplicates=False):
    searcher = KrkgwSearcher(data_dir_path, report_file_path,
                             allow_indirect_matches=allow_indirect_matches,
                             allow_duplicates=allow_duplicates)
    searcher.search()
    return searcher


def assert_report_file_content_equals(expected_report, report_file_path):
    with open(report_file_path, encoding='utf8') as file:
        actual_report = file.read()
        assert actual_report == expected_report, '\n>>>> ACTUAL REPORT:\n{}\n\n>>>> EXPECTED REPORT:\n{}'.format(actual_report, expected_report)
