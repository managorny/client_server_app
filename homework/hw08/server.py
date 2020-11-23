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
    FROM, MESSAGE, MESSAGE_CLIENT, TO
from common.utils import get_message, send_message

logger = logging.getLogger('messengerapp_server')
# stream_handler.setLevel(logging.INFO)   # - для теста в консоли.


@log
def process_client_message(message, list_of_messages, client_with_message, clients_list, account_names_list):
    logger.debug(f'Разбор сообщения от клиента {client_with_message}')

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message:
        if message[USER][ACCOUNT_NAME] not in account_names_list.keys():
            account_names_list[message[USER][ACCOUNT_NAME]] = client_with_message
            answer = send_message(client_with_message, {RESPONSE: 200})
            logger.info(answer)
        else:
            response = {RESPONSE: 400, ERROR: 'Пользователь с таким именем уже существует.'}
            send_message(client_with_message, response)
            clients_list.remove(client_with_message)
            client_with_message.close()
        return

    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_CLIENT in message and \
            FROM in message and TO in message:
        return list_of_messages.append(message)

    elif ACTION in message and message[ACTION] == 'exit' and ACCOUNT_NAME in message:
        clients_list.remove(account_names_list[message[ACCOUNT_NAME]])
        clients_list[message[ACCOUNT_NAME]].close()
        del clients_list[message[ACCOUNT_NAME]]
        return

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

    account_names_list = {}

    while True:
        try:
            client, client_address = sock.accept()
        except socket.error:
            pass
        else:
            logger.info(f'Установлено соедение с клиентом {client_address}')
            clients.append(client)

        get_message_list = []
        send_message_list = []
        # errors_list = []

        try:
            if clients:
                get_message_list, send_message_list, errors_list = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if get_message_list:
            for client_with_message in get_message_list:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message,
                                           clients, account_names_list)
                except Exception:
                    logger.info(f'Потеряно соединение с клиентом {client_with_message.getpeername()}.')
                    clients.remove(client_with_message)

        for msg in messages:
            try:
                if msg[FROM][ACCOUNT_NAME] in account_names_list and \
                        account_names_list[msg[TO][ACCOUNT_NAME]] in send_message_list:
                    send_message(account_names_list[msg[TO][ACCOUNT_NAME]], msg)

                    logger.info(f'Cообщение отправлено пользователю {msg[TO][ACCOUNT_NAME]} '
                                f'от пользователя {msg[FROM][ACCOUNT_NAME]}.')
                elif msg[TO][ACCOUNT_NAME] in account_names_list and \
                        account_names_list[msg[TO][ACCOUNT_NAME]] not in send_message_list:
                    raise ConnectionError
                else:
                    logger.error(
                        f'Пользователь {msg[TO][ACCOUNT_NAME]} не существует, отправка сообщения невозможна.')
            except Exception:
                logger.info(f'Потеряно соединение с клиентом {msg[TO][ACCOUNT_NAME]}.')
                clients.remove(account_names_list[msg[TO][ACCOUNT_NAME]])
                del account_names_list[msg[TO][ACCOUNT_NAME]]
        messages.clear()


if __name__ == '__main__':
    make_sock_get_msg_send_answer()
