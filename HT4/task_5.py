"""
Create a Python program that repeatedly prompts the user for a number until
a valid integer is provided. Use a try/except block to handle any ValueError
exceptions, and keep asking for input until a valid integer is entered. Display
the final valid integer.
"""


def number_input() -> int:
    try:
        value = input('Input int or float: ')
        return int(value)
    except ValueError:
        return number_input()
        

if __name__ == '__main__':
    print(f'Final number: {number_input()}')