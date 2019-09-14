# Utils for generating train and test csv's

import os, csv

# Gets a dictionary representation of any csv file with key as id and value as the column representing value_index
def get_path_from_root(filename):
    print(os.path.abspath(filename))
    return os.path.abspath(filename)

def get_dict(csvfile, value_index):
    data_csvfile = open(get_path_from_root(csvfile), 'r')
    data_csvreader = csv.reader(data_csvfile)
    data_url_dict = {}

    for count, row in enumerate(data_csvreader):
        if count != 0:
            data_url_dict[row[0]] = row[value_index]

    return data_url_dict