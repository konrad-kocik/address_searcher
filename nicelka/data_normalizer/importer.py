from os import path
from re import match


def import_results_from_text_file(file_dir, file_name):
    results = []

    with open(path.join(file_dir, file_name), encoding='utf8') as file:
        result = []

        for line in file:
            line = line.strip()
            _check_for_corrupted_line(line, file_dir, file_name)

            if _is_line_empty_in_result(line, result):
                continue
            elif _is_line_with_zip_code(line):
                result.append(line)
                if _has_multiple_line_name(result):
                    result = _convert_to_result_with_single_line_name(result)
                results = _add_to_results(results, result)
                result = []
            else:
                result.append(line)

    return results


def _check_for_corrupted_line(line, file_dir, file_name):
    if _is_line_corrupted(line):
        raise Exception("Line '{}' is corrupted, fix it in file {}".format(
            line, path.join(file_dir, file_name)))


def _is_line_corrupted(line):
    return match('^.+[0-9]{2} *- *[0-9]{3} *[A-Z a-z]+$', line)


def _is_line_empty_in_result(line, result):
    return not line and len(result) < 3


def _is_line_empty_between_results(line, result):
    return not line and len(result) >= 3


def _is_line_with_zip_code(line):
    return match('^[0-9]{2} *- *[0-9]{3} *[A-Z a-z]+$', line)


def _has_multiple_line_name(result):
    return len(result) > 3


def _convert_to_result_with_single_line_name(result):
    multi_line_name = result[:-2]
    address_and_zip_code = result[-2:]
    single_line_name = ' '.join(multi_line_name)
    return [single_line_name] + address_and_zip_code


def _add_to_results(results, result):
    if len(result) == 4:
        result[0] = result[0] + " " + result.pop(1)
    elif len(result) > 4:
        raise Exception("Incorrect result: {}".format(result))
    results.append(result)

    return results
