"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(),
в которую передается 5 параметров —
товар (item),
количество (quantity),
цена (price),
покупатель (buyer),
дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""

import json


def write_order_to_json(add_data):
    with open('task_2/orders.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open('task_2/orders.json', 'w', encoding='utf-8') as file:
        orders_list = data['orders']
        for i in add_data:
            print(i)
            order = {'item': i[0],
                     'quantity': i[1],
                     'price': i[2],
                     'buyer': i[3],
                     'date': i[4],
                     }
            orders_list.append(order)
        json.dump(data, file, indent=4, ensure_ascii=False)


add_data = [
    [
        "Телефон",
        "2",
        "45000",
        "Сергей Гуливанин",
        "12.12.2019"
    ],
    [
        "Ноутбук",
        "4",
        "67000",
        "Андрей Петров",
        "12.03.2020"
    ],
]

# В идеале сразу словарь засылать, но поэкспериментировал с list выше
# add_data = [
#     {
#         "item": "Телефон",
#         "quantity": "2",
#         "price": "45000",
#         "buyer": "Сергей Гуливанин",
#         "date": "12.12.2019"
#     },
# ]


write_order_to_json(add_data)
