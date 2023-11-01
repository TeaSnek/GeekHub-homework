"""
Write a Python program that demonstrates exception chaining. Create a custom
exception class called CustomError and another called SpecificError. In your
program (could contain any logic you want), raise a SpecificError, and then
catch it in a try/except block, re-raise it as a CustomError with the original
exception as the cause. Display both the custom error message and the original
exception message.
"""


class CustomError(BaseException):
    pass


class SpecificError(BaseException):
    pass


if __name__ == '__main__':
    try:
        try:
            raise SpecificError('Prikoldes')
        except SpecificError as e:
            print(e)
            raise CustomError(e)
    except CustomError as e:
        print(e)
