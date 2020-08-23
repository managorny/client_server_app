"""
4. Преобразовать слова
 «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
 и выполнить обратное преобразование (используя методы encode и decode).
"""

my_list = ['разработка', 'администрирование', 'protocol', 'standard']

encode_el = []
decode_el = []
for i in my_list:
    encode_el.append(i.encode('utf-8'))

for el in encode_el:
    decode_el.append(el.decode('utf-8'))

print(encode_el)
print(decode_el)
