"""
2. Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.
"""

my_list = [b'class', b'function', b'method']

for i in my_list:
    print(f'{i} - {type(i)} - {len(i)}')
