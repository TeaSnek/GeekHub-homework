"""
Створіть клас в якому буде атребут який буде рахувати кількість створених
екземплярів класів.
"""


class Self_Counter:
    counter = 0

    def __init__(self) -> None:
        Self_Counter.counter += 1

    def __del__(self):
        Self_Counter.counter -= 1


if __name__ == '__main__':
    cc = Self_Counter()
    print(cc.counter)
    ccc = Self_Counter()
    print(cc.counter)
    del ccc
    print(cc.counter)
