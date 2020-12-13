from os import path
from re import findall

from xlwt import Workbook


def export_results_to_excel_file(results, file_dir, file_name, sheet_name):
    workbook = Workbook()
    sheet = workbook.add_sheet(sheet_name)

    sheet.write(0, 0, 'Nazwa')
    sheet.write(0, 1, 'Ulica')
    sheet.write(0, 2, 'Kod pocztowy')
    sheet.write(0, 3, 'Miasto')

    for result_id, result in enumerate(results, start=1):
        for result_part_id, result_part in enumerate(result):
            if result_part_id == 2:
                _write_zip_code_and_city(sheet, result_id, result_part)
            else:
                sheet.write(result_id, result_part_id, result_part)

    workbook.save(path.join(file_dir, file_name))


def _write_zip_code_and_city(sheet, row_id, result_part):
    zip_code = findall('^.*[0-9]{2} *[-–] *[0-9]{3}', result_part)[0]
    city = result_part.replace(zip_code, '')
    sheet.write(row_id, 2, zip_code.strip())
    sheet.write(row_id, 3, city.strip())
