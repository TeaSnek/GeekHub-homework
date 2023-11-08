"""
Напишіть функцію,яка приймає на вхід рядок та повертає кількість окремих
регістро-незалежних букв та цифр, які зустрічаються в рядку більше ніж 1 раз.
Рядок буде складатися лише з цифр та букв (великих і малих). Реалізуйте
обчислення за допомогою генератора.

Example (input string -> result):
"abcde" -> 0            # немає символів, що повторюються
"aabbcde" -> 2          # 'a' та 'b'
"aabBcde" -> 2          # 'a' присутнє двічі і 'b' двічі (`b` та `B`)
"indivisibility" -> 1   # 'i' присутнє 6 разів
"Indivisibilities" -> 2 # 'i' присутнє 7 разів та 's' двічі
"aA11" -> 2             # 'a' і '1'
"ABBA" -> 2             # 'A' і 'B' кожна двічі
"""


def counter(line: str):
    while line != '':
        if line.count(line[0]) > 1:
            yield 1
        else:
            yield 0
        line = line.replace(line[0], '')


def splitter(line: str) -> int:
    line = line.lower()
    return sum(counter(line))


if __name__ == '__main__':
    print(splitter('abcde'))
    print(splitter('aabbcde'))
    print(splitter('aabBcde'))
    print(splitter('indivisibility'))
    print(splitter('Indivisibilities'))
    print(splitter('aA11'))
    print(splitter('ABBA'))
