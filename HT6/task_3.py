"""
Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від 0 до 1000,
и яка вертатиме True, якщо це число просте і False - якщо ні.
"""

from math import sqrt


def is_prime(n):
    if n <= 1 or (n%2==0 and n!=2):
        return False
    elif n==2:
        return True
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True
 
 
if __name__ == '__main__':
    print(is_prime(11))
