import socketserver
import threading
import datetime
import struct
from collections import namedtuple

PACKET_HEAD = b'zz'

ServiceTransaction = namedtuple('ServiceTransaction', ('''datetimetime,
                                 term_id, transaction_id,
                                 transaction_type, data'''))

PayTransaction = namedtuple('PayTransaction', ('''datetimetime,
    term_id, transaction_id,
                                 transaction_type,  id_, summ'''))


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


def decode_service_transaction(packet):
    serv_struct = struct.Struct('! BH3BHI2B')
    unpacked = serv_struct.unpack(packet)
    unpack_date = date_decode(unpacked[1])
    date = datetime.datetime(*unpack_date)
    unpacked_time = time_decode(*unpacked[2:5])
    time = datetime.timedelta(seconds=unpacked_time)
    date = date + time
    print('')
    print('Дата транзакции: {}'.format(date))
    print('ID терминала: {}'.format(unpacked[5]))
    print('ID транзакции: {}'.format(unpacked[6]))
    print('Тип транзакции: {}'.format(unpacked[7]))
    print('Вид транзакции: {}'.format(unpacked[8]))


def decode_pay_transaction(packet):
    pay_struct = struct.Struct('! BH3BHIBIQ')
    unpacked = pay_struct.unpack(packet)
    unpack_date = date_decode(unpacked[1])
    date = datetime.datetime(*unpack_date)
    unpacked_time = time_decode(*unpacked[2:5])
    time = datetime.timedelta(seconds=unpacked_time)
    date = date + time
    print(unpacked)
    print('Дата транзакции: {}'.format(date))
    print('ID терминала: {}'.format(unpacked[5]))
    print('ID транзакции: {}'.format(unpacked[6]))
    print('Тип транзакции: {}'.format(unpacked[7]))
    if unpacked[7] == 1:
        print('id Организации для перевода: {}'.format(unpacked[8]))
        print('Сумма перевода: {}'.format(unpacked[9]))
    if unpacked[7] == 2:
        print('id сотрудника-инкассатора: {}'.format(unpacked[8]))
        print('Сумма инкассации: {}'.format(unpacked[9]))


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.data = self.request.recv(1024).decode()
        self.data = self.request.recv(1024)
        print('Клиент {} сообщает {}'.format(self.client_address[0], self.data))
        lenght = len_decode(self.data)
        if lenght == 13:
            decode_service_transaction(self.data[2:])
        elif lenght == 24:
            decode_pay_transaction(self.data[2:])
        # first_chunk = dcode_first(self.data)

        # packet_decode(self.data)
        # self.request.sendall(bytes(self.data.upper(), 'utf-8'))
        self.request.sendall(self.data)


class MyThreadedTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        print('Работает поток {}'.format(cur_thread))
        print('Клиент {} сообщает {}'.format(self.client_address[0], data))
        lenght = len_decode(data)
        if lenght == 13:
            decode_service_transaction(data[2:])
        elif lenght == 24:
            decode_pay_transaction(data[2:])
        self.request.sendall(data)


class MyThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    server = MyThreadedTCPServer((HOST, PORT), MyThreadedTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    print(server.server_address)
    server_thread.daemon = True
    server_thread.start()
    print('Сервер запущен в многопоточном режиме. поток {}'.format(server_thread.name))
    # server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    # print('Сервер запущен')
    # print(server.server_address)
    while server_thread.is_alive():
        pass
    # server.serve_forever()
    
    server.shutdown()
    server.server_close()
    print('DONE!')
