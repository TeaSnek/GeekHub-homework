"""
Запишіть в один рядок генератор списку (числа в діапазоні від 0 до 100), сума
цифр кожного елемент якого буде дорівнювати 10.

Результат: [19, 28, 37, 46, 55, 64, 73, 82, 91]
"""


def digit_num(number: int):
    return sum(int(digit) for digit in str(number))


if __name__ == '__main__':
    print([x for x in range(100) if digit_num(x) == 10])
