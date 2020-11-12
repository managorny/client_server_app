import sys
import logging
import logs.log_configs.client_log_config
import logs.log_configs.server_log_config

if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('messengerapp_server')
else:
    logger = logging.getLogger('messengerapp_client')

# В виде функции
def log(function):
    def wrapper(*args, **kwargs):
        result = function(*args, ** kwargs)
        return logger.debug(f'Функция {function.__name__}, Результат - {result}')
    return wrapper


# @log
# def my_func(a, b):
#     return a + b

# В виде класса
