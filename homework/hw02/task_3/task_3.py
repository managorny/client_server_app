"""
3. Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
второму — целое число, третьему — вложенный словарь,
где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""

import yaml

data = {'items': ['phone', 'laptop', 'ears'],
        'items_quantity': 32,
        'items_ptice': {'phone': '100\u20ac',
                        'laptop': '1200\u20ac',
                        'ears': '70\u20ac'}
        }

with open('file.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)

with open("file.yaml", 'r', encoding='utf-8') as file:
    data_new = yaml.load(file, Loader=yaml.SafeLoader)
    # data_new = yaml.load(file, Loader=yaml.FullLoader)

print(data == data_new)
