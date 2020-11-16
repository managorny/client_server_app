import sys
import json
import socket
import time
import logs.log_configs.client_log_config
import logging
# from logs.log_configs.client_log_config import stream_handler # - для теста в консоли.
from decorators import log
import argparse

from common.default_conf import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, DEFAULT_CLIENT_MODE, MESSAGE, MESSAGE_CLIENT, FROM
from common.utils import get_message, send_message

logger = logging.getLogger('messengerapp_client')
# stream_handler.setLevel(logging.INFO)   # - для теста в консоли.

account_name = 'Demo'

@log
def create_message(sock, client_account_name):
    client_message = input("Введите сообщение или \'Q\' для завершения работы ")
    if client_message == 'Q':
        sock.close()
        logger.info("Завершение работы по запросу.")
        print("Программа завершена")
        sys.exit(0)
    else:
        message = {
            ACTION: MESSAGE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: client_account_name
            },
            MESSAGE_CLIENT: client_message,
        }
    return message


@log
def create_presence_message(client_account_name):
    presence_message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: client_account_name
        }
    }
    logger.info(f'Сообщение о присутствии пользователя {client_account_name} сформировано')
    return presence_message

@log
def get_message_from_server(response):
    if ACTION in response and FROM in response and MESSAGE_CLIENT in response \
            and response[ACTION] == MESSAGE:
        sender = response[FROM]
        text_message = response[MESSAGE_CLIENT]
        print(f'Получено сообщение от {sender}, текст сообщения: {text_message}')
        logger.info(f'Получено сообщение от {sender}, текст сообщения: {text_message}')
    else:
        logger.error(f'Не удается распознать ответ от сервера: {response}')


@log
def get_response(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            response = '200 : OK'
            logger.info(response)
            return response
        error = f'400 : {message[ERROR]}'
        logger.info(error)
        return error
    raise logger.error(ValueError)


@log
def load_params():  # TODO try to use argparse
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if '-m' in sys.argv:
            mode = sys.argv[sys.argv.index('-m') + 1]
        if mode not in ('listen', 'send'):
            logger.critical(f'Указан недопустимый режим работы {mode}, '
                            f'допустимые режимы: listen , send')
            sys.exit(1)
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        logger.warning('Использованы дефолтные адрес и порт')
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        mode = DEFAULT_CLIENT_MODE
    except ValueError:
        logger.critical('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    return server_address, server_port, mode


def make_sock_send_msg_get_answer():
    # 192.168.1.109 8081 (при проверке: работает как через терминал, так и через PyCharm)

    server_address, server_port, mode = load_params()

    logger.info(
        f'Запущен клиент с парамертами: адрес сервера - {server_address}, '
        f'порт - {server_port}, режим работы - {mode}')

    # Инициализация сокета и обмен
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, server_port))
    message_to_server = create_presence_message(account_name)
    send_message(sock, message_to_server)

    try:
        get_response(get_message(sock))
    except (ValueError, json.JSONDecodeError):
        logger.error('Не удалось декодировать сообщение сервера.')
    else:
        if mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            if mode == 'send':
                try:
                    send_message(sock, create_message(sock, account_name))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger.error(f'Соединение с сервером {server_address} потеряно.')
                    sys.exit(1)

            if mode == 'listen':
                try:
                    get_message_from_server(get_message(sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger.error(f'Соединение с сервером {server_address} потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    make_sock_send_msg_get_answer()
