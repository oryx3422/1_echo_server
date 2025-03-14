import socket


def get_host():
    host_input = input("Введите адрес хоста [по умолчанию 'localhost']: ")
    if not host_input.strip():
        return 'localhost'
    else:
        return host_input


def get_port():
    while True:
        try:
            port_input = input("Введите номер порта [по умолчанию 12345]: ")
            if not port_input.strip():
                port = 12345
            else:
                port = int(port_input)
            if 1 <= port <= 65535:
                return port
            else:
                print("Пожалуйста, введите номер порта от 1 до 65535.")
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите числовое значение номера порта.")


host = get_host()
port = get_port()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((host, port))
    print("Connected to server")
except ConnectionRefusedError:
    print(f"Не удалось подключиться к серверу {host}:{port}. Проверьте адрес и порт.")
    sock.close()
    exit()

received_data = ''

while True:
    msg = input("Your string (type 'exit' to quit):")
    try:
        sock.send((msg + '\n').encode('utf-8'))
        print("Message sent to server")
    except BrokenPipeError:
        print("Соединение с сервером было потеряно.")
        break

    full_response = ''
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Сервер закрыл соединение.")
                sock.close()
                exit()
            received_data += data.decode('utf-8')
            if '\n' in received_data:
                line, received_data = received_data.split('\n', 1)
                full_response = line
                break
        except ConnectionResetError:
            print("Соединение было разорвано сервером.")
            sock.close()
            exit()

    print("Message received from server")
    print(full_response)

    if msg.lower() == 'exit':
        break

sock.close()
print("Connection closed to server")
