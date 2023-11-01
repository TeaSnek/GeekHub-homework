"""
Написати функцію <prime_list>, яка прийматиме 2 аргументи - початок і кінець
діапазона, і вертатиме список простих чисел всередині цього діапазона. Не
забудьте про перевірку на валідність введених даних та у випадку
невідповідності - виведіть повідомлення.
"""
from math import sqrt


def prime_list(start: int, end: int) -> list:
    if start >= end:
        raise ValueError('Beginning must have lower value than ending')
    
    elif end < 1:
        return []
    
    elif end == 1:
        return [1]
    
    elif end == 2:
        return [1, 2]
    
    
    out = list()                                              
    sieve = [True] * (end + 1)                          #сітка для викреслювання
    stop = int(sqrt(end + 1))
    
    for p in range(3, stop, 2):                              #метод ератосфена
        if sieve[p] and p % 2 == 1:
            for i in range(p * p, end + 1, p):
                sieve[i] = False

    for i in range(start - start % 2 + 1, end + 1, 2):
        if sieve[i]:
            out.append(i)

    return out


if __name__ == '__main__':
    print(prime_list(5, 22))
