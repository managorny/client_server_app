import sys
import os
import unittest
# добавляем путь, чтобы видеть внешние папки, например, дойти до common
sys.path.append(os.path.join(os.getcwd(), '../..'))
from common.default_conf import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR
from server import process_client_message

action = ACTION
presence = PRESENCE
time_msg = TIME
user = USER
account_name_msg = ACCOUNT_NAME
response = RESPONSE
error = ERROR


class TestServer(unittest.TestCase):
    # тестовые данные
    ok_dict = {response: 200}
    error_dict = {
        response: 400,
        error: 'Bad Request'
    }

    def test_ok_message(self):
        self.assertEqual(process_client_message(
            {action: presence, time_msg: '123.123', user: {account_name_msg: 'Demo'}}), self.ok_dict)

    def test_without_action(self):
        self.assertEqual(process_client_message(
            {time_msg: '123.123', user: {account_name_msg: 'Demo'}}), self.error_dict)

    def test_wrong_action(self):
        self.assertEqual(process_client_message(
            {action: 'test_not_ok_action', time_msg: '123.123', user: {account_name_msg: 'Demo'}}), self.error_dict)

    def test_without_time(self):
        self.assertEqual(process_client_message(
            {action: presence, user: {account_name_msg: 'Demo'}}), self.error_dict)

    def test_without_user(self):
        self.assertEqual(process_client_message(
            {action: presence, time_msg: '123.123'}), self.error_dict)

    def test_not_ok_user(self):
        self.assertEqual(process_client_message(
            {action: presence, time_msg: '123.123', user: {account_name_msg: 'TestNotOkUser'}}), self.error_dict)


if __name__ == '__main__':
    unittest.main()
