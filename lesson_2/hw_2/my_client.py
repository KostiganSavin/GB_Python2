import socket
import struct
import datetime
from collections import namedtuple

HOST, PORT = 'localhost', 9999
PACKET_HEAD = b'zz'
# data = input('Введите сообщение для сервера:')
ServiceTransaction = namedtuple('ServiceTransaction', ('''lenght,
                                 term_id, transaction_id, date, time_1,
                                 time_2, time_3, transaction_type, data'''))

PayTransaction = namedtuple('PayTransaction', ('''lenght,
                                 term_id, transaction_id, date, time_1,
                                 time_2, time_3, transaction_type,
                                 id_, summ'''))


def date_encode(year, month, day):
    year -= 2000
    date = (year << 9) | (month << 5) | (day & 31)
    return date


def time_encode(sec):
    first = ((sec & 0xff0000) >> 16)
    second = ((sec & 0xff00) >> 8)
    third = (sec & 0xff)
    return (first, second, third)


def make_packet(data):
    if data.transaction_type == 0:
        packet = struct.pack('2sBHIHI2B', data.head, data.lenght, data.term_id,
                             data.transaction_id, data.date, data.time,
                             data.transaction_type, data.data)
    elif data.transaction_type == 1:
        packet = struct.pack('2sBHIHIBIQ', data.head, data.lenght, data.term_id,
                             data.transaction_id, data.date, data.time,
                             data.transaction_type, data.organization_id, data.summ)
    elif data.transaction_type == 2:
        packet = struct.pack('2sBHIHIBIQ', data.head, data.lenght,
                             data.term_id, data.transaction_id, data.date,
                             data.time, data.transaction_type, data.person_id, data.summ)      
    return packet


d = datetime.date(2017, 4, 3)
date = date_encode(d.year, d.month, d.day)
t = time_encode(20012)

lst = [13, 1, 1, date]
lst.extend(t)
lst.extend([0, 2])
st = ServiceTransaction(*lst)
st_pack = struct.Struct('BHIH3B2B')
packet = st_pack.pack(*st)
packet = PACKET_HEAD + packet
print(packet)
# pt = PayTransaction(b'zz', 24, 1, 1, date, t, 1, 101, 20000)
# t_lst = [st, pt, it]

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
# print('Распаковано:', data)