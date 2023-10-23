"""
Write a script which accepts a <number> from user and generates dictionary in
range <number> where key is <number> and value is <number>*<number>

e.g. 3 --> {0: 0, 1: 1, 2: 4, 3: 9}
"""


if __name__ == '__main__':
    number = int(input('Input target integer number: '))
    dict_result = {x: x*x for x in range(number+1)}
    print('Result: ', dict_result)