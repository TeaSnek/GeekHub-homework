"""
Створити клас Calc, який буде мати атребут last_result та 4 методи. Методи
повинні виконувати математичні операції з 2-ма числами, а саме додавання,
віднімання, множення, ділення.
- Якщо під час створення екземпляру класу звернутися до атребута last_result
він повинен повернути пусте значення.
- Якщо використати один з методів - last_result повенен повернути результат
виконання ПОПЕРЕДНЬОГО методу.
    Example:
    last_result --> None
    1 + 1
    last_result --> None
    2 * 3
    last_result --> 2
    3 * 4
    last_result --> 6
    ...
- Додати документування в клас
"""


class Calc:
    def __init__(self) -> None:
        self.last_result = None
        self.__this_result = None

    def my_sum(self, first, second):
        self.last_result, self.__this_result = self.__this_result, \
            first + second
        return self.__this_result

    def my_dif(self, first, second):
        self.last_result, self.__this_result = self.__this_result, \
            first - second
        return self.__this_result

    def my_mult(self, first, second):
        self.last_result, self.__this_result = self.__this_result, \
            first * second
        return self.__this_result

    def my_div(self, first, second):
        self.last_result, self.__this_result = self.__this_result, \
            first / second
        return self.__this_result


if __name__ == '__main__':
    calc = Calc()
    print(calc.last_result)
    print(calc.my_sum(1, 1))
    print(calc.last_result)
    print(calc.my_dif(2, 2))
    print(calc.last_result)
    print(calc.my_mult(3, 3))
    print(calc.last_result)
    print(calc.my_div(4, 4))
    print(calc.last_result)
