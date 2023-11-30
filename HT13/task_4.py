"""
Create 'list'-like object, but index starts from 1 and index of 0 raises error.
Тобто це повинен бути клас, який буде поводити себе так, як list (маючи
основні методи), але індексація повинна починатись із 1
"""


class My_list(list):
    def __getitem__(self, key):
        if key > 0:
            return list.__getitem__(self, key-1)
        elif key < 0:
            return list.__getitem__(self, key)
        else:
            raise IndexError('My_list indextion starts with 1')


x = My_list((1, 2, 3, 4))
print(x[-1])

print(x[1])

print(x[0])
