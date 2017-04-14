import socket
import struct
import datetime
# from collections import namedtuple

HOST, PORT = 'localhost', 9999 
PACKET_HEAD = b'zz'
# data = input('Введите сообщение для сервера:')


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


def encode_service_transaction(pack_struct):
    message = dict()
    message['lenght'] = pack_struct.size - 1
    d = datetime.date(2017, 4, 3)
    message['date'] = date_encode(d.year, d.month, d.day)
    message['time'] = time_encode(20012)
    message['term_id'] = 1
    message['transact_id'] = 1
    message['transact_type'] = 0
    message['transact_data'] = 0
    print(message)
    return message


def encode_pay_transaction(pack_struct):
    message = dict()
    message['lenght'] = pack_struct.size - 1
    d = datetime.date(2017, 4, 3)
    message['date'] = date_encode(d.year, d.month, d.day)
    message['time'] = time_encode(20012)
    message['term_id'] = 1
    message['transact_id'] = 2
    message['transact_type'] = 2
    message['id_'] = 101
    message['summ'] = 20005
    print(message['lenght'])
    print(message)
    return message


serv_struct = struct.Struct('! BH3BHI2B')
pay_struct = struct.Struct('! BH3BHIBIQ')

mess = encode_service_transaction(serv_struct)
mess1 = encode_pay_transaction(pay_struct)

packet = serv_struct.pack(mess['lenght'], mess['date'], *mess['time'],
                          mess['term_id'], mess['transact_id'],
                          mess['transact_type'], mess['transact_data'])
packet1 = pay_struct.pack(mess1['lenght'], mess1['date'], *mess1['time'],
                          mess1['term_id'], mess1['transact_id'],
                          mess1['transact_type'], mess1['id_'], mess1['summ'])

packet = PACKET_HEAD + packet
packet1 = PACKET_HEAD + packet1
# print('serv', packet)
# print('pay', packet1)

pack = [packet, packet1]
print(pack)

for item in pack:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
# sock.sendall(bytes(data + '\n', 'utf-8'))
        sock.sendall(item)
# recived = str(sock.recv(1024), 'utf-8')
        recived = sock.recv(1024)

        print('Отправлено:{}'.format(item))
        print('Получено:  {}'.format(recived))

# sock.close()

# data = struct.unpack('2sh', recived)
# print('Распаковано:', data
