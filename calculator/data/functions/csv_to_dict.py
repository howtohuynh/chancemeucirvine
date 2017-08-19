import csv

def list_to_dict(l1: list, l2: list) -> dict:
    result = {}
    for index in range(len(l2)):
        result[l2[index]] = l1[index]
    return result

def csv_to_dict(file: str, dictKeyList: list) -> dict:
    result = {}
    open_file = open(file, 'r')
    read_file = csv.reader(open_file)
    csv_format = next(read_file) #skips first line (header) in a .csv file
    if csv_format[1] in ['gender', 'ethnicity', 'major']:
        for line in read_file:
            if line[0] not in result:
                result[line[0]] = {}
                result[line[0]][line[1]] = list_to_dict(line[2:], dictKeyList)
            else:
                result[line[0]][line[1]] = list_to_dict(line[2:], dictKeyList)
    else:
        for line in read_file:
            if line[0] not in result:
                result[line[0]] = {}
                result[line[0]] = list_to_dict(line[1:], dictKeyList)
            else:
                result[line[0]] = list_to_dict(line[1:], dictKeyList)
    return result