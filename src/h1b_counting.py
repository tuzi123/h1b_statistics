"""
@author: Xiaoming Su
"""

import sys
import csv

def process_file(file, header_list, N=10):
    '''
    This function reads H1B csv file and finds top N states and occupations
    for certified visa applications
    :param file: str, this is the path of input csv file
    :param header_list: list, this is a list of column headers that should be
                        read from input file
    :param N: int, return top N results
    :return: tuple (total_certified, sorted_work_states, sorted_soc_names)
             WHERE
             int, total_certified: the total number of certified H1B cases
             list, sorted_work_states: a sorted list of states and number of certified cases,
                                       e.g., [(str1, int1), (str2, int2)...]
             list, sorted_soc_names: a sorted list of occupations and number of certified cases,
                                       e.g.,[(str1, int1), ...]
    '''
    columns = {}
    work_states = {}
    soc_names = {}
    attribute = ["CASE_STATUS", "SOC_NAME", "WORKSITE_STATE"]

    try:
        with open(file, mode='r', encoding="utf8") as input:
            reader = csv.DictReader(input, delimiter=";")
            total_certified = 0
            header = reader.fieldnames

            # Try to find correct header
            for i in range(len(header_list[0])):
                if header_list[0][i] in header:
                    attribute[0] = header_list[0][i]
            for i in range(len(header_list[1])):
                if header_list[1][i] in header:
                    attribute[1] = header_list[1][i]
            for i in range(len(header_list[2])):
                if header_list[2][i] in header:
                    attribute[2] = header_list[2][i]

            for row in reader:
                for (key, value) in row.items():
                    if key in attribute:
                        if key not in columns:
                            columns[key] = [value]
                        else:
                            columns[key].append(value)
                if columns[attribute[0]][-1] == "CERTIFIED":
                    if columns[attribute[2]][-1] not in work_states:
                        work_states[columns[attribute[2]][-1]] = 1
                    else:
                        work_states[columns[attribute[2]][-1]] += 1
                    if columns[attribute[1]][-1] not in soc_names:
                        soc_names[columns[attribute[1]][-1]] = 1
                    else:
                        soc_names[columns[attribute[1]][-1]] += 1
                    total_certified += 1
            sorted_work_states = sorted(work_states.items(), key=lambda k: (-k[1], k))[:N]
            sorted_soc_names = sorted(soc_names.items(), key=lambda k: (-k[1], k))[:N]

            return total_certified, sorted_work_states, sorted_soc_names
    except IOError:
        print('No such file: {}'.format(file))
        sys.exit(0)


def write_file(output_path, header, list, total_count):
    """
    This function calculates % of applications that have been certified and
    writes results into the specified output file.

    :param output_path: str, the path of the output file
    :param header: str, the header of the ouput file
    :param list: list, the sorted list of results that should be calculated and
                 written into the file, e.g., [(str1, int1), ...]
    :param total_count: the total number of certified cases
    """
    with open(output_path, 'w') as output:
        output.write(header + "\n")
        for key, occurences in list:
            percentage = round(float(occurences / total_count * 100), 1)
            output.write("{};{};{}%\n".format(key, occurences, percentage))


def main(argv):
    """
    This is the main function used to call process_file() and write_file()
    :param argv: list, list of input csv file path and output file path
    """
    # if the columns has different header names in different files, just add it below
    case_status_header = ["CASE_STATUS", "STATUS"]
    soc_name_header = ["SOC_NAME", "LCA_CASE_SOC_NAME"]
    work_states_header = ["WORKSITE_STATE", "LCA_CASE_WORKLOC1_STATE"]
    attribute = [case_status_header, soc_name_header, work_states_header]
    total_certified, work_states, soc_names = process_file(argv[1], attribute)

    header_occupations = "TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"
    write_file(argv[2], header_occupations, soc_names, total_certified)

    header_states = "TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"
    write_file(argv[3], header_states, work_states, total_certified)


if __name__ == "__main__":
    main(sys.argv)





