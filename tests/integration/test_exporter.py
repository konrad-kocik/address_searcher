from os import path

from nicelka.data_normalizer.exporter import export_results_to_excel_file


data_dir = path.join('data', 'exporter')


def test_export_results_to_excel_file():
    results = [
        ['Urząd Miejski w Koninie', 'Plac Wolności 1', '62-500 Konin'],
        ['Fundacja "Aleją Zdrowia - Od Juniora Do Seniora"', 'ul. Os. Legionów 12/1', '62-510 Konin'],
        ['Fundacja "Aluminium"', 'ul. Margaretkowa 7/4', '62-510 Konin'],
        ['Fundacja "Bądź Zaradny"', 'ul. Bydgoska 2a', '62-510 Konin'],
        ['Fundacja "Głos Koniński"', '3 Maja 1-3', '62-500 Konin'],
        ['Fundacja "Jeszcze Raz" i spółka', 'ul. Kwiatkowskiego 3/10', '62 - 504 Konin']
    ]
    file_name = 'export_results_to_excel_file.xls'
    export_results_to_excel_file(results, data_dir, file_name)

    # TODO: add assert with excel check
