import socket

sock = socket.socket()
sock.setblocking(1)

print("КЛИЕНТ: Попытка соединения с сервером на адресе localhost:9090...")
sock.connect(('localhost', 9090))
print("КЛИЕНТ: Соединение с сервером установлено.")

msg = input("Введите строку для отправки серверу: ")

print("КЛИЕНТ: Отправка данных серверу...")
sock.send(msg.encode())
print("КЛИЕНТ: Данные успешно отправлены серверу.")

print("КЛИЕНТ: Ожидание ответа от сервера...")
data = sock.recv(1024)
print("КЛИЕНТ: Данные получены от сервера.")

sock.close()
print("КЛИЕНТ: Соединение с сервером закрыто.")

print("Ответ от сервера:", data.decode())

