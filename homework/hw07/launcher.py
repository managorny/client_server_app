import time
import os
from subprocess import Popen

text_for_choice = """
1 - запуск сервера
2 - остановка сервера
3 - запуск 3 пишуших клиентов и 3 слушающих
4 - остановка клиентов
5 - остановить все и выйти
Выберите действие: \n"""

clients = []
server = ''
path_to_file = os.path.dirname(__file__)
path_to_script_server = os.path.join(path_to_file, "server.py")
path_to_script_client = os.path.join(path_to_file, "client.py")

while True:
    choice = input(text_for_choice)

    if choice == '1':
        print("Запустили сервер")
        server = Popen(
            f'osascript -e \'tell application "Terminal" to do'
            f' script "python3 {path_to_script_server} -p 8081 -address 192.168.1.109"\'', shell=True)
    elif choice == '2':
        print("Убили сервер")
        server.kill()
    elif choice == '3':
        print("Запустили клиенты")
        for i in range(3):
            clients.append(
                Popen(
                    f'osascript -e \'tell application "Terminal" to do'
                    f' script "python3 {path_to_script_client} 192.168.1.109 8081 -m send"\'',
                    shell=True))
            # Задержка для того, что бы отправляющий процесс успел
            # зарегистрироваться на сервере, и потом в словаре имен
            # клиентов остался только слушающий клиент
            time.sleep(0.5)
        for i in range(3):
            clients.append(
                Popen(
                    f'osascript -e \'tell application "Terminal" to do'
                    f' script "python3 {path_to_script_client} 192.168.1.109 8081 -m listen"\'',
                    shell=True))
            # Задержка для того, что бы отправляющий процесс успел
            # зарегистрироваться на сервере, и потом в словаре имен
            # клиентов остался только слушающий клиент
            time.sleep(0.5)
    elif choice == '4':
        for i in range(len(clients)):
            print(clients[i])
            clients[i].kill()
    elif choice == '5':
        for i in range(len(clients)):
            clients[i].kill()
        server.kill()
        break
