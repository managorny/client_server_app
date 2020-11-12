import socket
import sys
import json
import logs.log_configs.server_log_config
import logging
# from logs.log_configs.server_log_config import stream_handler # - для теста в консоли.

from common.default_conf import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS
from common.utils import get_message, send_message

logger = logging.getLogger('messengerapp_server')
# stream_handler.setLevel(logging.INFO)   # - для теста в консоли.


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Demo':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def load_params():

    # валидация и загрузка порта
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        logger.error('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        logger.critical('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # валидация и загрузка адреса
    try:
        if '-address' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-address') + 1]
        else:
            listen_address = DEFAULT_IP_ADDRESS

    except IndexError:
        logger.error('После параметра -\'address\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)
    return listen_address, listen_port


def make_sock_get_msg_send_answer():
    # -p 8081 -address 192.168.1.109 (при проверке: работает как через терминал, так и через PyCharm)

    # Готовим сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(load_params())

    # Слушаем порт
    sock.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = sock.accept()
        try:
            message_from_client = get_message(client)
            logger.info(f'Сообщение: {message_from_client}')
            response_from_client = process_client_message(message_from_client)
            send_message(client, response_from_client)
            client.close()
        except (ValueError, json.JSONDecodeError):
            logger.error('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    make_sock_get_msg_send_answer()
