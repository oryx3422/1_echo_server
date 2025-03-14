import socket  # Импорт модуля для работы с сокетами

# == Запуск сервера ===
print("СЕРВЕР: Запуск сервера...")  # Служебное сообщение о запуске сервера

# Создаём TCP-сокет
sock = socket.socket()

# Привязываем сокет к адресу и порту 9090.
# Пустая строка '' означает, что сервер принимает подключения на всех доступных интерфейсах.
sock.bind(('', 9090))
print("СЕРВЕР: Сокет привязан к порту 9090.")  # Сообщение о привязке порта

# Начинаем прослушивание входящих подключений.
# Значение backlog = 0 указывает, что сервер ожидает только одно подключение.
sock.listen(0)
print("СЕРВЕР: Начало прослушивания входящих подключений.")  # Сообщение о начале прослушивания

# Ожидаем подключения клиента (блокирующий вызов).
conn, addr = sock.accept()
print(f"СЕРВЕР: Подключился клиент с адресом {addr}.")  # Сообщение о подключении клиента

# Переменная для накопления полученных данных
msg = ''

# Запускаем цикл для получения данных от клиента порциями по 1024 байта (~1 КБ)
while True:
    data = conn.recv(1024)  # Получаем данные (до 1024 байт за раз)
    
    # Если данных не получено, значит клиент завершил передачу или отключился
    if not data:
        print("СЕРВЕР: Клиент прекратил отправку данных или отключился.")
        break

    # Выводим служебное сообщение о приёме данных
    print(f"СЕРВЕР: Получена порция данных от клиента: {data.decode()}")

    # Накопление полученных данных в переменной msg
    msg += data.decode()

    # Отправляем обратно ту же порцию данных клиенту (поведение эхо-сервера)
    conn.send(data)
    print("СЕРВЕР: Порция данных отправлена обратно клиенту.")

# После завершения приема всех данных выводим полное сообщение от клиента
print("СЕРВЕР: Полное сообщение, полученное от клиента:")
print(msg)

# Закрываем соединение с клиентом
conn.close()
print("СЕРВЕР: Клиент отключился.")

# Останавливаем сервер, закрывая основной сокет
sock.close()
print("СЕРВЕР: Остановка сервера. Работа завершена.")
