"""
Create a Python script that takes an age as input. If the age is less than 18
or greater than 120, raise a custom exception called InvalidAgeError. Handle
the InvalidAgeError by displaying an appropriate error message.
"""


class InvalidAgeError(BaseException):
    pass


if __name__ == '__main__':
    age = int(input('Input your age: '))
    try:
        if not 18 <= age <= 120:
            raise InvalidAgeError
    except InvalidAgeError:
        print('Invalid age input')
