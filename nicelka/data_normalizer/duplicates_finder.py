from nicelka.data_normalizer.importer import import_results_from_text_file


def find_duplicates(report_file_name, report_file_dir='data'):
    results = import_results_from_text_file(report_file_dir, report_file_name)
    duplicates = _get_duplicates_from_results(results)
    _save_duplicates(duplicates)
    _show_duplicates(duplicates)


def _get_duplicates_from_results(results):
    duplicates = []

    for i, result in enumerate(results):
        for other in results[i+1:]:
            if result[1] == other[1] and result[2] == other[2]:
                if result not in duplicates:
                    duplicates.append(result)
                if other not in duplicates:
                    duplicates.append(other)
                break

    duplicates.sort(key=lambda x: x[1] + x[2])
    return duplicates


def _show_duplicates(duplicates):
    for duplicate_id, duplicate in enumerate(duplicates):
        print("Duplikat nr {}".format(duplicate_id + 1))
        print(duplicate[0])
        print(duplicate[1])
        print(duplicate[2])
        print('')


def _save_duplicates(duplicates):
    with open('../duplicates.txt', mode='w', encoding='utf8') as file:
        for duplicate_id, duplicate in enumerate(duplicates):
            file.write("Duplikat nr {}".format(duplicate_id + 1) + '\n')
            file.write(duplicate[0] + '\n')
            file.write(duplicate[1] + '\n')
            file.write(duplicate[2] + '\n\n')
