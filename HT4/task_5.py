"""
Create a Python program that repeatedly prompts the user for a number until
a valid integer is provided. Use a try/except block to handle any ValueError
exceptions, and keep asking for input until a valid integer is entered. Display
the final valid integer.
"""

from task_1 import number_input


if __name__ == '__main__':
    print(f'Final number: {number_input()}')