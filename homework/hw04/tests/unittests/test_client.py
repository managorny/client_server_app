import sys
import os
import unittest
# добавляем путь, чтобы видеть внешние папки, например, дойти до common
sys.path.append(os.path.join(os.getcwd(), '../..'))
from common.default_conf import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR
from client import create_presence_message, get_answer

action = ACTION
presence = PRESENCE
time_msg = TIME
user = USER
account_name_msg = ACCOUNT_NAME
response = RESPONSE
error = ERROR


class TestClient(unittest.TestCase):

    def test_ok_message(self):
        test_msg = create_presence_message()
        test_msg[time_msg] = '123.123'  # необходимо задать конкретное время, чтобы проверить
        self.assertEqual(test_msg, {action: presence, time_msg: '123.123', user: {account_name_msg: 'Demo'}})

    def test_answer_200(self):
        self.assertEqual(get_answer({response: 200}), '200 : OK')

    def test_answer_400(self):
        self.assertEqual(get_answer({response: 400, error: 'Bad Request'}), '400 : Bad Request')

    def test_without_response(self):
        with self.assertRaises(ValueError):
            get_answer({})


if __name__ == '__main__':
    unittest.main()
