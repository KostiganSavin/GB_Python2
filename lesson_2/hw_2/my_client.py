import socket
import struct
import datetime
from collections import namedtuple

HOST, PORT = 'localhost', 9999
PACKET_HEAD = b'zz'
# data = input('Введите сообщение для сервера:')
message = dict()

PayTransaction = namedtuple('PayTransaction', ('''lenght,
                                 term_id, transaction_id, date, time_1,
                                 time_2, time_3, transaction_type,
                                 id_, summ'''))


def date_encode(year, month, day):
    '''
    Кодлирование даты в формате год - 7 бит, мемяц - 4 бита, число - 5 бит
    '''
    year -= 2000
    date = (year << 9) | (month << 5) | (day & 31)
    return date


def time_encode(sec):
    '''
    Кодирование времени в 3-байта, время в секундах
    '''
    first = ((sec & 0xff0000) >> 16)
    second = ((sec & 0xff00) >> 8)
    third = (sec & 0xff)
    return (first, second, third)


pack_struct = struct.Struct('! BH3BHI2B')
message['lenght'] = pack_struct.size - 1
d = datetime.date(2017, 4, 3)
message['date'] = date_encode(d.year, d.month, d.day)
message['time'] = time_encode(20012)
message['term_id'] = 1
message['transact_id'] = 1
message['transact_type'] = 0
message['transact_data'] = 0
print(message)


packet = pack_struct.pack(message['lenght'], message['date'], *message['time'],
                          message['term_id'], message['transact_id'],
                          message['transact_type'], message['transact_data'])
packet = PACKET_HEAD + packet
print(packet)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
# sock.sendall(bytes(data + '\n', 'utf-8'))
sock.sendall(packet)
# recived = str(sock.recv(1024), 'utf-8')
recived = sock.recv(1024)


print('Отправлено:{}'.format(packet))
print('Получено:  {}'.format(recived))
sock.close()

# data = struct.unpack('2sh', recived)
# print('Распаковано:', data
