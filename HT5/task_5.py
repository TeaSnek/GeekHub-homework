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


def verbal_calculator(expr : str) -> int | float:
    if re.fullmatch(r'(\d.\d|\d)\s*(\+|\*|\*\*|/|-|%|//)\s*(\d.\d|\d)', expr):
        x, y = [number for number in              #getting numbers form string
                re.split(r'\s*[\+|\*|\*\*|//|-|%|/]\s*', expr) if number]

        try:
            x, y = int(x), int(y)
        except ValueError:
            x, y = float(x), float(y)

        match re.findall(r'[\+|\*|\*\*|/|-|%|//]', expr):
            case ['+']:
                return x + y
            case ['-']:
                return x - y
            case ['/']:
                try:
                    return x / y
                except ZeroDivisionError:
                    return float('nan')
            case ['/', '/']:
                try:
                    return x // y
                except ZeroDivisionError:
                    return float('nan')
                except ValueError:
                    return float('nan')
            case ['*']:
                return x * y
            case ['*', '*']:
                return x ** y
    raise UnsupportedTemplateError


if __name__ == '__main__':
    task = input('Input expression you want to evaluate: ')
    value = verbal_calculator(task)
    print(task, value, sep=' | ')
    