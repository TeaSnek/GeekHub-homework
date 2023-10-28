"""
Користувач вводить змiннi "x" та "y" з довiльними цифровими значеннями. 
Створiть просту умовну конструкцiю (звiсно вона повинна бути в тiлi ф-цiї),
пiд час виконання якої буде перевiрятися рiвнiсть змiнних "x" та "y" та у 
випадку нервіності - виводити ще і різницю.

Повиннi опрацювати такi умови (x, y, z заміність на відповідні числа):
x > y;       вiдповiдь - "х бiльше нiж у на z"
x < y;       вiдповiдь - "у бiльше нiж х на z"
x == y.      вiдповiдь - "х дорiвнює z"
"""


def number_input() -> int | float:
        try:
            value = input('Input int or float: ')
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                try:
                    return number_input()
                except RecursionError:
                    return 0


def task_3_func(x, y) -> None:
    if x > y:
        print(f'{x} більше {y} на {x - y}')
    elif x < y:
        print(f'{y} більше {x} на {y - x}')
    else:
        print(f'{x} дорiвнює {y}')


if __name__ == '__main__':
    x = number_input()
    y = number_input()
    task_3_func(x, y)
    