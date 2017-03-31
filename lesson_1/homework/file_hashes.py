import os
import hashlib


FILE_NAME_WITH_PARTS = 'parts.md5'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
list_files = os.listdir(os.path.join(BASE_DIR, 'files/file2'))
_files = dict()

for file in list_files:
    if not (file == FILE_NAME_WITH_PARTS):
        # print(file)
        with open(os.path.join(BASE_DIR, 'files/file2', file), 'rb') as f:
            b = f.read()
            h = hashlib.md5(b)
            # print(h.hexdigest())
        _files[h.hexdigest()] = file

# print(_files)

file_with_hash = os.path.join(BASE_DIR, 'files/file2', FILE_NAME_WITH_PARTS)
with open(file_with_hash) as file_hashes:
    for line in file_hashes:
        print(_files[line.strip()])
        with open(os.path.join(BASE_DIR, 'files/file2', 'out_file'), 'ab') as out_file:
             f = open(os.path.join(BASE_DIR, 'files/file2', _files[line.strip()]), 'rb').read()
             out_file.write(f)



# print(lst)
# for item in lst:
# print(_files[item])