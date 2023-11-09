"""
Напишіть функцію,яка прймає рядок з декількох слів і повертає довжину
найкоротшого слова. Реалізуйте обчислення за допомогою генератора.
"""

import string


def word_len_splitter(line: str):
    for word in [w.strip(string.punctuation) for w in line.split()]:
        yield len(word)


def shortest(line: str):
    return min(word_len_splitter(line))


print(shortest('my shortest words'))
