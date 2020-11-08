"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet
"""

import subprocess
import chardet

direct_list = ['yandex.ru', 'youtube.com']
for direct in direct_list:
    args = ['ping', direct]
    ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    z = 0
    for i in ping.stdout:
        if z == 6:
            break
        else:
            identify = chardet.detect(i)
            interm_res = i.decode(identify['encoding']).encode('utf-8')

            # second variant
            # x = list(identify.values())
            # print(x)
            # interm_res = i.decode(f'{x[0]}').encode('utf-8')

            print(interm_res.decode('utf-8'))
            z += 1
