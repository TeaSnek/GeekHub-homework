"""
Написати функцію, яка приймає на вхід список (через кому), підраховує
кількість однакових елементів у ньомy і виводить результат. Елементами списку
можуть бути дані будь-яких типів.
Наприклад:

1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> 
"1 -> 3, foo -> 2, [1, 2] -> 2, True -> 1"
"""

from collections import Counter


def counter(lst: list) -> dict:
    stringified_list = list(map(str, lst))
    counter_dict = {key : stringified_list.count(key) 
                    for key in stringified_list}
    print(*[f'{key} -> {counter_dict[key]}' for key in counter_dict.keys()], sep=', ')


if __name__ == '__main__':
    counter([1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2]])