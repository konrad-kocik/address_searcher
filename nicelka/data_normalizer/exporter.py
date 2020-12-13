from os import path

from xlwt import Workbook


def export_results_to_excel_file(results, file_dir, file_name):
    workbook = Workbook()
    sheet = workbook.add_sheet('Sheet1')

    sheet.write(0, 0, 'Nazwa')
    sheet.write(0, 1, 'Ulica')
    sheet.write(0, 2, 'Kod pocztowy')

    for result_id, result in enumerate(results, start=1):
        for result_part_id, result_part in enumerate(result):
            sheet.write(result_id, result_part_id, result_part)

    workbook.save(path.join(file_dir, file_name))
