import select
import socket
import sys
import json
import time
import logs.log_configs.server_log_config
import logging
# from logs.log_configs.server_log_config import stream_handler # - для теста в консоли.
from decorators import log


from common.default_conf import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS, \
    FROM, MESSAGE, MESSAGE_CLIENT, DEFAULT_CLIENT_MODE
from common.utils import get_message, send_message

logger = logging.getLogger('messengerapp_server')
# stream_handler.setLevel(logging.INFO)   # - для теста в консоли.


@log
def process_client_message(message, list_of_messages, client_with_message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Demo':
        answer = send_message(client_with_message, {RESPONSE: 200})
        logger.info(answer)
        return answer
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_CLIENT in message:
        return list_of_messages.append((message[USER][ACCOUNT_NAME], message[MESSAGE_CLIENT]))
    else:
        error = send_message(client_with_message, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        logger.info(error)
        return error


@log
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

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(load_params())
    sock.settimeout(0.5)
    sock.listen(MAX_CONNECTIONS)

    clients = []
    messages = []

    while True:
        try:
            client, client_address = sock.accept()
            logger.info(f'Установлено соедение с клиентом {client_address}')
            clients.append(client)
        except socket.error as socketerror:
            pass

        get_message_list = []
        send_message_list = []
        # errors_list = []

        try:
            if clients:
                get_message_list, send_message_list, errors_list = select.select(clients, clients, [], 0)

            if get_message_list:
                for client_with_message in get_message_list:
                    try:
                        process_client_message(get_message(client_with_message), messages, client_with_message)
                    except:
                        logger.info(f'Потеряно соединение с клиентом {client_with_message. getpeername()}.')
                        clients.remove(client_with_message)

            if messages and send_message_list:
                message = {
                    ACTION: MESSAGE,
                    FROM: messages[0][0],
                    TIME: time.time(),
                    MESSAGE_CLIENT: messages[0][1]
                }
                del messages[0]
                for waiting_client in send_message_list:
                    try:
                        send_message(waiting_client, message)
                    except:
                        logger.info(f'Потеряно соединение с клиентом {waiting_client.getpeername()}.')
                        clients.remove(waiting_client)
        except (ValueError, json.JSONDecodeError):
            logger.error('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    make_sock_get_msg_send_answer()
