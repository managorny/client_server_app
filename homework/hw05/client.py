import sys
import json
import socket
import time
import logs.log_configs.client_log_config
import logging
# from logs.log_configs.client_log_config import stream_handler # - для теста в консоли.

from common.default_conf import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message

logger = logging.getLogger('messengerapp_client')
# stream_handler.setLevel(logging.INFO)   # - для теста в консоли.


def create_presence_message(account_name='Demo'):
    presence_message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return presence_message


def get_answer(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return logger.error(f'400 : {message[ERROR]}')
    raise logger.error(ValueError)


def load_params():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        logger.warning('Использованы дефолтные адрес и порт')
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        logger.critical('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
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
        logger.info(answer)
    except (ValueError, json.JSONDecodeError):
        logger.error('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    make_sock_send_msg_get_answer()
