"""
Ну і традиційно - калькулятор Повинна бути 1 ф-цiя,
яка б приймала 3 аргументи - один з яких операцiя, яку зробити! Аргументи
брати від юзера (можна по одному - 2, окремо +, окремо 2; можна всі разом -
типу 1 + 2). Операції що мають бути присутні: +, -, *, /, %, //, **. Не 
забудьте протестувати з різними значеннями на предмет помилок!
"""

import re


class UnsupportedTemplateError(BaseException):
    pass


def verbal_calculator(task : str) -> int | float:
    if re.fullmatch(r'(\d.\d|\d)\s*(\+|\*|\*\*|/|-|%|//)\s*(\d.\d|\d)', task):
        result = eval(task)
        return result
    raise UnsupportedTemplateError


if __name__ == '__main__':
    print('+ ', verbal_calculator('2+2'))
    print('- ', verbal_calculator('2-2'))
    print('* ', verbal_calculator('2*2'))
    print('** ', verbal_calculator('2**2'))
    print('/ ', verbal_calculator('2/2'))
    print('// ', verbal_calculator('2//2'))
    print('% ', verbal_calculator('2%2'))
    