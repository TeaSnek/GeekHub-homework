"""
Написати функцію <fibonacci>, яка приймає один аргумент і виводить всі числа
Фібоначчі, що не перевищують його.
"""


def fibonacci(n):
    if n < 0:
        return []
    elif n == 0:
        return [0]
    
    result = [0, 1]
    while sum(result[-2:]) <= n:
        result.append(sum(result[-2:]))
    return result


if __name__ == '__main__':
    print(fibonacci(5))
    print(fibonacci(0))
    print(fibonacci(-1))
