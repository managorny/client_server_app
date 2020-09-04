import sys
import json
import socket
import time

from common.default_conf import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message

action = ACTION
presence = PRESENCE
time_msg = TIME
user = USER
account_name_msg = ACCOUNT_NAME
response = RESPONSE
error = ERROR
default_ip_address = DEFAULT_IP_ADDRESS
default_port = DEFAULT_PORT


def create_presence_message(account_name='Demo'):
    presence_message = {
        action: presence,
        time_msg: time.time(),
        user: {
            account_name_msg: account_name
        }
    }
    return presence_message


def get_answer(message):
    if response in message:
        if message[response] == 200:
            return '200 : OK'
        return f'400 : {message[error]}'
    raise ValueError


def load_params():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)
    return server_address, server_port


def make_sock_send_msg_get_answer():
    # 192.168.1.109 8081 (при проверке: работает как через терминал, так и через PyCharm)

    # Инициализация сокета и обмен
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((load_params()))
    message_to_server = create_presence_message()
    send_message(sock, message_to_server)

    try:
        answer = get_answer(get_message(sock))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    make_sock_send_msg_get_answer()
