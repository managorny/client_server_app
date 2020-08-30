"""
6. Создать текстовый файл test_file.txt,
заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

import chardet
# from chardet import detect

my_list = ['сетевое программирование', 'сокет', 'декоратор']

with open('test_file.txt', 'w') as file:
    for i in my_list:
        file.write(f'{i}\n')
file.close()

with open('test_file.txt', 'rb') as file:
    encoding = chardet.detect(file.read())['encoding']
    print(f"кодировка {encoding}")
file.close()

with open('test_file.txt', 'r', encoding=encoding) as file:
    print(file.read())

# with open('test_file.txt', 'r', encoding='utf-8') as file:
#     print(file.read())
