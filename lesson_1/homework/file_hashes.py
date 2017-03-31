import os
import hashlib


FILE_NAME_WITH_PARTS = 'parts.md5'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)


def concat_file(dirname, file_hashes, out_file):
    """
    Функция соединяющая частички файла в единый файл
    на основании содержания фала с ХЭШ

    """
    list_files = os.listdir(os.path.join(BASE_DIR, 'files', dirname))
    _files = dict()

    for file in list_files:
        if not (file == file_hashes):
            with open(os.path.join(BASE_DIR, 'files',
                                   dirname, file), 'rb') as f:
                b = f.read()
                h = hashlib.md5(b)
            _files[h.hexdigest()] = file
    file_with_hash = os.path.join(BASE_DIR, 'files',
                                  dirname, file_hashes)
    with open(file_with_hash) as file_hash:
        for line in file_hash:
            print(_files[line.strip()])
            with open(os.path.join(BASE_DIR, 'files', dirname,
                                   out_file), 'ab') as out_f:
                f = open(os.path.join(BASE_DIR, 'files', dirname,
                                      _files[line.strip()]), 'rb').read()
                out_f.write(f)


def split_file(file, size):
    pass


def count_hash(dirname, name_hasgfile):
    pass


if __name__ == '__main__':
    # concat_file('file1', 'parts.md5', 'result_file')
    concat_file('file2', 'parts.md5', 'result_file')
