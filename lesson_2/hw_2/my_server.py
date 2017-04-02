import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).decode()
        print('Клиент {} сообщает {}'.format(self.client_address[0], self.data))
        self.request.sendall(bytes(self.data.upper(), 'utf-8'))
       

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print('Сервер запущен')
        server.serve_forever()
