import socket

HOST, PORT = 'localhost', 9999
data = input('Введите сообщение для сервера:')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.sendall(bytes(data + '\n', 'utf-8'))
recived = str(sock.recv(1024), 'utf-8')

print('Отправлено:{}'.format(data))
print('Получено:  {}'.format(recived))
