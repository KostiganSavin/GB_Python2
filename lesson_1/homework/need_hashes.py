import hashlib
import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path_to_file = os.path.join(BASE_DIR, 'need_hashes.csv')


def find_hash(hash_name, data):
    """
    Функция вычисляющая хэш для заданной строки.

    """
    if type(data) is bytes:
        h = hashlib.new(hash_name, data)
    else:
        h = hashlib.new(hash_name, data.encode('utf8'))
    return h.hexdigest()


lst = []
with open(path_to_file) as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        if not row[2]:
            row[2] = find_hash(row[1], row[0])
            lst.append(row)
        else:
            lst.append(row)

with open(path_to_file, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')

    for item in lst:
        writer.writerow(item)

# print(lst)
