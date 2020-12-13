from os import path

from nicelka.data_normalizer.importer import import_results_from_text_file


data_dir = path.join('data', 'importer')


def test_import_results_from_text_file():
    expected_results = [
        ['Urząd Miejski w Koninie', 'Plac Wolności 1', '62-500 Konin'],
        ['Fundacja "Aleją Zdrowia - Od Juniora Do Seniora"', 'ul. Os. Legionów 12/1', '62-510 Konin'],
        ['Fundacja "Aluminium"', 'ul. Margaretkowa 7/4', '78-310 Łowów Podlaski'],
        ['Fundacja "Bądź Zaradny"', 'ul. Bydgoska 2a', '62–510 Konin'],
        ['Fundacja "Głos Koniński"', '3 Maja 1-3', '62-500Konin'],
        ['Fundacja "Jeszcze Raz" i spółka', 'ul. Kwiatkowskiego 3/10', '62 - 504 Konin']
    ]

    assert import_results_from_text_file(data_dir, 'import_results_from_text_file.txt') == expected_results
