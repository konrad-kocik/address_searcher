from nicelka.data_normalizer.importer import import_results_from_text_file
from nicelka.data_normalizer.exporter import export_results_to_excel_file

name = 'Otrębusy po edycji'

results = import_results_from_text_file('data', 'report_text_file.txt')
export_results_to_excel_file(results, 'data', '{}.xls'.format(name), name)
