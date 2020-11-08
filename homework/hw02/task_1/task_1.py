"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить
в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
В этой же функции создать главный список для хранения данных отчета — например, main_data —
и поместить в него названия столбцов отчета в виде списка:
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""

import re
import csv

import chardet


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    for i in range(1, 4):
        with open(f'task_1/info_{i}.txt', 'rb') as file:
            encoding = chardet.detect(file.read())['encoding']

        with open(f'task_1/info_{i}.txt', 'r', encoding=encoding) as file:
            data = file.read()

        # хотел целиком записать название ОС, кроме этого варианта быстро не придумал ничего
        with open(f'task_1/info_{i}.txt', 'r', encoding=encoding) as file:
            for row in file:
                if row.find('Название ОС:') == 0:
                    name_os_str = row.split(':')[1]
                    name_os = (re.sub(r'(^\s*)|((\n)|( \n))', '', name_os_str))
                    os_name_list.append(name_os)

        os_prod_list.append(re.compile(r'Изготовитель системы:\s*\S*').findall(data)[0].split()[2])

        os_code_list.append(re.compile(r'Код продукта:\s*\S*').findall(data)[0].split()[2])

        # добавляем слово PC
        os_type_name = re.compile(r'Тип системы:\s*.*\n').findall(data)[0]
        os_type_list.append(os_type_name.split()[2] + ' ' + os_type_name.split()[3])

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)

    j = 1
    for i in range(3):
        row_data = [j, os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]]
        main_data.append(row_data)
        j += 1
    return main_data, encoding


def write_to_csv(out_file):
    main_data, encoding = get_data()
    with open(out_file, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in main_data:
            # print(row) # проверка того, что записываем в конечный файл
            writer.writerow(row)


write_to_csv('task_1/report.csv')

# проверяем кодировку файла
# with open('report.csv', 'rb') as file:
#     encoding = chardet.detect(file.read())['encoding']
#     print(f"кодировка {encoding}")
