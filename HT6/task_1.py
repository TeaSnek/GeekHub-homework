"""
Написати функцію <square>, яка прийматиме один аргумент - сторону квадрата,
і вертатиме 3 значення у вигляді кортежа: периметр квадрата, площа квадрата
та його діагональ.
"""


def square(length):
    if length < 0:
        raise ValueError(f'Incorrect square side length {length}')

    perimeter = length * 4
    area = length ** 2
    diagonal = length * 2 ** 0.5

    return perimeter, area, diagonal


if __name__ == '__main__':
    x = 2
    y = 15.5
    z = -25
    print(square(x))
    print(square(y))
    print(square(z))
