import socketserver
import threading
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
    month = ((input_str & 0x1e0) >> 5)
    day = ((input_str & 0x1f))
    return (year, month, day)


def time_decode(first, second, third):
    time = (first << 16) | (second << 8) | (third)
    return time


def len_decode(data):
    chunk = struct.Struct('B')
    print(chunk.unpack(data[2:3])[0])
    return chunk.unpack(data[2:3])[0]


def decode_first(data):
    s_struct = struct.Struct('BHIH3B2B')
    unpacked = ServiceTransaction._make(s_struct.unpack(data[2:]))
    unpacked_date = date_decode(unpacked.date)
    date = datetime.datetime(*unpacked_date)
    unpacked_time = time_decode(unpacked.time_1,
                                    unpacked.time_2, unpacked.time_3)
    time = datetime.timedelta(seconds=unpacked_time)
    date = date + time
    print('Длина пакета транзакции: {}'.format(unpacked.lenght))
    print('Дата транзакции: {}'.format(date))
    print('ID терминала: {}'.format(unpacked.term_id))
    print('ID транзакции: {}'.format(unpacked.transaction_id))
    print('Тип транзакции: {}'.format(unpacked.transaction_type))
    print('Вид транзакции: {}'.format(unpacked.data))


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.data = self.request.recv(1024).decode()
        self.data = self.request.recv(1024)
        print('Клиент {} сообщает {}'.format(self.client_address[0], self.data))
        # lenght = len_decode(self.data)
        # first_chunk = dcode_first(self.data)

        # packet_decode(self.data)
        # self.request.sendall(bytes(self.data.upper(), 'utf-8'))
        self.request.sendall(self.data)


class MyThreadedTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        print('Работает поток {}'.format(cur_thread))
        self.request.sendall(data)


class MyThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    HOST, PORT = 'localhost', 0

    server = MyThreadedTCPServer((HOST, PORT), MyThreadedTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    print(server.server_address)
    server_thread.daemon = True
    server_thread.start()
    print('Сервер запущен в многопоточном режиме. поток {}'.format(server_thread.name))
    # server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    # print('Сервер запущен')
    # print(server.server_address)

    server.serve_forever()
    
    server.shutdown()
    server.server_close()
    print('DONE!')
