import socket
import logging
import sys

logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

port = get_port()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

while True:
    try:
        sock.bind(('', port))
        break
    except OSError as e:
        if e.errno == 98:
            logging.warning(f"Порт {port} уже занят, пробуем следующий порт.")
            port += 1
        else:
            logging.error(f"Ошибка при привязке к порту {port}: {e}")
            sys.exit(1)

print(f"Сервер слушает порт {port}")
logging.info("Server is starting")

sock.listen(1)
logging.info(f"Port {port} is listening")

while True:
    try:
        conn, addr = sock.accept()
        logging.info("Client is accepted")
        logging.info(f"Client address: {addr[0]}")
        logging.info(f"Client port: {addr[1]}")

        msg = ''

        while True:
            data = conn.recv(1024)
            if not data:
                logging.info("All data is accepted")
                break
            msg += data.decode('utf-8')
            while '\n' in msg:
                line, msg = msg.split('\n', 1)
                logging.info(f"Received from client: {line}")
                print(f"Получено сообщение от пользователя - '{line}'")
                if line.lower() == 'exit':
                    logging.info("Exit command received. Closing connection.")
                    conn.send("Server closing connection.\n".encode('utf-8'))
                    break
                else:
                    response = line.upper()
                    conn.send((response + '\n').encode('utf-8'))
                    logging.info("Response sent to client")
            if line.lower() == 'exit':
                break

        conn.close()
        logging.info("Connection is closed. Client is off")
        logging.info("Waiting for new client...")
    except KeyboardInterrupt:
        logging.info("Server is shutting down.")
        print("\nСервер завершает работу.")
        break
    except Exception as e:
        logging.error(f"An error occurred: {e}")

sock.close()
logging.info("Server is off")
logging.info("Goodbye")
logging.info("ByeBye!")
