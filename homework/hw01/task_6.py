"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но открыть нужно ИМЕННО в формате Unicode (utf-8)

например, with open('test_file.txt', encoding='utf-8') as t_f
невыполнение условия - минус балл
"""

import chardet

my_list = ['сетевое программирование', 'сокет', 'декоратор']

default_encoding = 'cp866'

with open ('test_file.txt', 'w', encoding=default_encoding) as file:
    for i in my_list:
        file.write(f'{i}\n')
file.close()

# можно определить кодировку и сразу открыть файл в нужной кодировке

# with open('test_file.txt', 'rb') as file:
#     encoding = chardet.detect(file.read())['encoding']
#     print(f"кодировка {encoding}")
# file.close()

# with open('test_file.txt', 'r', encoding=encoding) as file:
#     print(file.read())


# можно перезаписать файл в utf-8
def encode_file(file_in):
    with open(file_in, 'rb') as file_out:
        read = file_out.read()
        encoding = chardet.detect(read)['encoding']
        print(f"кодировка {encoding}")
    content = read.decode(encoding)
    with open('test_file.txt', 'w', encoding='utf-8') as file_out:
        file_out.write(content)


encode_file('test_file.txt')

with open('test_file.txt', 'r', encoding='utf-8') as file:
    print(file.read())
