
# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
# соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и
# также проверить тип и содержимое переменных.

import chardet

data = ['разработка', 'сокет', 'декоратор']

for i in data:
    temp = ""
    for j in i:
        print(str(j.encode("unicode_escape")))  # b'\\u0434'
        temp += str(j.encode("unicode_escape"))[3:-1] # посимвольно привожу оригинальную строку к виду юникод код-поинтов
    print(f"\noriginal string: {i}\ntype: {type(i)}\n{chardet.detect(i.encode())}\nuni: {temp}\ntype: {type(temp)}\n")





