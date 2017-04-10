import socket
import struct
import datetime
from collections import namedtuple

HOST, PORT = 'localhost', 9999
PACKET_HEAD = b'zz'
# data = input('Введите сообщение для сервера:')
ServiceTransaction = namedtuple('ServiceTransaction', ('''head, lenght,
                                 term_id, transaction_id, date, time,
                                 transaction_type, data'''))

PayTransaction = namedtuple('PayTransaction', ('''head, lenght,
                                 term_id, transaction_id, date, time,
                                 transaction_type, organization_id, summ'''))

InkassTransaction = namedtuple('InkassTransaction', ('''head, lenght,
                                 term_id, transaction_id, date, time,
                                 transaction_type, person_id, summ'''))


def date_encode(year, month, day):
    year -= 2000
    date = (year << 9) | (month << 5) | (day & 31)
    return date


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
t = (20012 & 0xffffff)

st = ServiceTransaction(b'zz', 12, 1, 1, date, t, 0, 0) 
pt = PayTransaction(b'zz', 24, 1, 1, date, t, 1, 101, 20000)
it = InkassTransaction(b'zz', 24, 1, 1, date, t, 2, 102, 20000)
t_lst = [st, pt, it]

for item in t_lst:
    data = make_packet(item)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
# sock.sendall(bytes(data + '\n', 'utf-8'))
    sock.sendall(data)
# recived = str(sock.recv(1024), 'utf-8')
    recived = sock.recv(1024)


    print('Отправлено:{}'.format(data))
    print('Получено:  {}'.format(recived))
    sock.close()

# data = struct.unpack('2sh', recived)
# print('Распаковано:', data)