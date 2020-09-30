"""Программа-сервер"""

import socket
import sys
import json

from common.default_conf import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS
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
max_connections = MAX_CONNECTIONS


def process_client_message(message):
    if action in message and message[action] == presence and time_msg in message \
            and user in message and message[user][account_name_msg] == 'Demo':
        return {response: 200}
    return {
        response: 400,
        error: 'Bad Request'
    }


def load_params():

    # валидация и загрузка порта
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = default_port
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # валидация и загрузка адреса
    try:
        if '-address' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-address') + 1]
        else:
            listen_address = default_ip_address

    except IndexError:
        print(
            'После параметра -\'address\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)
    return listen_address, listen_port


def make_sock_get_msg_send_answer():
    # -p 8081 -address 192.168.1.109 (при проверке: работает как через терминал, так и через PyCharm)

    # Готовим сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(load_params())

    # Слушаем порт
    sock.listen(max_connections)

    while True:
        client, client_address = sock.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response_from_client = process_client_message(message_from_client)
            send_message(client, response_from_client)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    make_sock_get_msg_send_answer()
