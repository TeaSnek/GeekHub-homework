"""
Create a custom exception class called NegativeValueError. Write a Python 
program that takes an integer as input and raises the NegativeValueError if the
input is negative. Handle this custom exception with a try/except block and
display an error message.
"""


class NegativeValueError(BaseException):
    pass


if __name__ == '__main__':
    try:
        if int(input('Input integer value: ')) < 0:
            raise NegativeValueError
    except:
        print('Negative number input')