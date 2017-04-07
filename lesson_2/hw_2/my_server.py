import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.data = self.request.recv(1024).decode()
        self.data = self.request.recv(1024)
        print('Клиент {} сообщает {}'.format(self.client_address[0], self.data))
        # self.request.sendall(bytes(self.data.upper(), 'utf-8'))
        self.request.sendall(self.data)

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print('Сервер запущен')

    server.serve_forever()
