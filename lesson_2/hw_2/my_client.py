import socket
import struct
import datetime
from collections import namedtuple

HOST, PORT = 'localhost', 9999
PACKET_HEAD = b'zz'
# data = input('Введите сообщение для сервера:')


def date_encode(year, month, day):
    year -= 2000
    date = (year << 9) | (month << 5) | (day & 31)
    return date


d = datetime.date(2017, 4, 3)
date = date_encode(d.year, d.month, d.day)

data = struct.pack('2si', PACKET_HEAD, date,)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
# sock.sendall(bytes(data + '\n', 'utf-8'))
sock.sendall(data)
# recived = str(sock.recv(1024), 'utf-8')
recived = sock.recv(1024)


print('Отправлено:{}'.format(data))
print('Получено:  {}'.format(recived))

data = struct.unpack('2si', recived)
print('Распаковано:', data)