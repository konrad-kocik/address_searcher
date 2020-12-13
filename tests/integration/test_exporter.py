from os import path

from pytest import fixture

from nicelka.data_normalizer.exporter import export_results_to_excel_file
from tests.integration.utilities.utilities import remove_file, assert_excel_file_content_equals


data_dir = path.join('data', 'exporter')
export_results_to_excel_file_name = 'export_results_to_excel_file.xls'


@fixture
def remove_files_after(request):
    def teardown():
        remove_file(path.join(data_dir, export_results_to_excel_file_name))
    request.addfinalizer(teardown)


def test_export_results_to_excel_file(remove_files_after):
    results = [
        ['Urząd Miejski w Koninie', 'Plac Wolności 1', '62-500 Konin'],
        ['Fundacja "Aleją Zdrowia - Od Juniora Do Seniora"', 'ul. Os. Legionów 12/1', '62-510 Konin'],
        ['Fundacja "Aluminium"', 'ul. Margaretkowa 7/4', '78-310 Łowów Podlaski'],
        ['Fundacja "Bądź Zaradny"', 'ul. Bydgoska 2a', '62–510 Konin'],
        ['Fundacja "Głos Koniński"', '3 Maja 1-3', '62-500Konin'],
        ['Fundacja "Jeszcze Raz" i spółka', 'ul. Kwiatkowskiego 3/10', '62 - 504 Konin']
    ]
    expected_excel_content = [
        ['Nazwa', 'Ulica', 'Kod pocztowy', 'Miasto'],
        ['Urząd Miejski w Koninie', 'Plac Wolności 1', '62-500', 'Konin'],
        ['Fundacja "Aleją Zdrowia - Od Juniora Do Seniora"', 'ul. Os. Legionów 12/1', '62-510', 'Konin'],
        ['Fundacja "Aluminium"', 'ul. Margaretkowa 7/4', '78-310', 'Łowów Podlaski'],
        ['Fundacja "Bądź Zaradny"', 'ul. Bydgoska 2a', '62–510', 'Konin'],
        ['Fundacja "Głos Koniński"', '3 Maja 1-3', '62-500', 'Konin'],
        ['Fundacja "Jeszcze Raz" i spółka', 'ul. Kwiatkowskiego 3/10', '62 - 504', 'Konin']
    ]
    export_results_to_excel_file(results, data_dir, export_results_to_excel_file_name, 'sheet')
    assert_excel_file_content_equals(expected_excel_content, path.join(data_dir, export_results_to_excel_file_name))
