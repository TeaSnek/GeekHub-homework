"""
Написати функцію <square>, яка прийматиме один аргумент - сторону квадрата,
і вертатиме 3 значення у вигляді кортежа: периметр квадрата, площа квадрата
та його діагональ.
"""


def square(length):
    if length < 0: 
        raise ValueError(f'Incorrect square side length {length}')
    
    return (length*4, length**2, length*2**(1/2))


if __name__ == '__main__':
    x = 2
    y = 15.5 
    z = -25
    print(square(x))
    print(square(y))
    print(square(z))