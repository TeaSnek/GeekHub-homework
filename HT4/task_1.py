"""
Написати скрипт, який приймає від користувача два числа (int або float) і
робить наступне:
Кожне введене значення спочатку пробує перевести в int. У разі помилки -
пробує перевести в float, а якщо і там ловить помилку - пропонує ввести
значення ще раз (зручніше на даному етапі навчання для цього використати цикл
while). Виводить результат ділення першого на друге. Якщо при цьому виникає
помилка - оброблює її і виводить відповідне повідомлення
"""


def number_input() -> int | float:
    try:
        value = input('Input int or float: ')
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return number_input()


if __name__ == '__main__':
    x, y = number_input(), number_input()
    try:
        print(x/y)
    except ZeroDivisionError as e:
        print(e)
