import socket

print("СЕРВЕР: Запуск сервера...")

sock = socket.socket()
sock.bind(('localhost', 9090))
print("СЕРВЕР: Сокет привязан к порту 9090.")

sock.listen(0)
print("СЕРВЕР: Начало прослушивания входящих подключений.")

conn, addr = sock.accept()
print(f"СЕРВЕР: Подключился клиент с адресом {addr}.")

msg = ''

while True:
    data = conn.recv(1024)
    if not data:
        print("СЕРВЕР: Клиент прекратил отправку данных или отключился.")
        break
    print(f"СЕРВЕР: Получена порция данных от клиента: {data.decode()}")
    msg += data.decode()
    conn.send(data)
    print("СЕРВЕР: Порция данных отправлена обратно клиенту.")

print("СЕРВЕР: Полное сообщение, полученное от клиента:")
print(msg)

conn.close()
print("СЕРВЕР: Клиент отключился.")

sock.close()
print("СЕРВЕР: Остановка сервера. Работа завершена.")