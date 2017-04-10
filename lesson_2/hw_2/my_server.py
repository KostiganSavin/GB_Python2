import socketserver
import datetime
import struct
from collections import namedtuple 

PACKET_HEAD = b'zz'

ServiceTransaction = namedtuple('ServiceTransaction', ('''lenght,
                                 term_id, transaction_id, date, time_1,
                                 time_2, time_3, transaction_type, data'''))

PayTransaction = namedtuple('PayTransaction', ('''lenght,
                                 term_id, transaction_id, date, time_1,
                                 time_2, time_3, transaction_type,
                                 id_, summ'''))


def date_decode(input_str):
    year = ((input_str & 0xfe00) >> 9)
    year += 2000
    # print(year)
    month = ((input_str & 0x1e0) >> 5)
    # print(month)
    day = ((input_str & 0x1f))
    # print(day)
    return (year, month, day)


def time_decode(first, second, third):
    time = (first << 16) | (second << 8) | (third)
    return time


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.data = self.request.recv(1024).decode()
        self.data = self.request.recv(1024)
        print('Клиент {} сообщает {}'.format(self.client_address[0], self.data))
        s_struct = struct.Struct('BHIH3B2B')
        un1 = ServiceTransaction._make(s_struct.unpack(self.data[2:]))
        ud = date_decode(un1.date)
        date = datetime.datetime(*ud)
        ut = time_decode(un1.time_1, un1.time_2, un1.time_3)
        time = datetime.timedelta(seconds=ut)
        date = date + time
        print('Длина пакета транзакции: {}'.format(un1.lenght))
        print('Дата транзакции: {}'.format(date))
        print('ID терминала: {}'.format(un1.term_id))
        print('ID транзакции: {}'.format(un1.transaction_id))
        print('Тип транзакции: {}'.format(un1.transaction_type))
        print('Вид транзакции: {}'.format(un1.data))

        # self.request.sendall(bytes(self.data.upper(), 'utf-8'))
        self.request.sendall(self.data)

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print('Сервер запущен')

    server.serve_forever()
