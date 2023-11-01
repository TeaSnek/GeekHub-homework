"""
Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від 0 до 1000,
и яка вертатиме True, якщо це число просте і False - якщо ні.
"""
from math import sqrt


def is_prime(number):
    if number <= 1 or (number % 2 == 0 and number != 2):
        return False
    
    elif number==2:
        return True
    
    for i in range(3, int(sqrt(number)) + 1, 2):
        if number % i == 0:
            return False
        
    return True
 
 
if __name__ == '__main__':
    print(is_prime(11))
