"""
Створити клас Person, в якому буде присутнім метод __init__ який буде приймати
якісь аргументи, які зберігатиме в відповідні змінні.
- Методи, які повинні бути в класі Person - show_age, print_name,
show_all_information.
- Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть
атрибут profession (його не має інсувати під час ініціалізації).
"""


class Person:
    def __init__(self, age, name) -> None:
        self.age = age
        self.name = name

    def show_age(self):
        print(f'age: {self.age}')

    def print_name(self):
        print(f'name: {self.name}')

    def show_all_information(self):
        for item in self.__dict__:
            print(f'{item}: {getattr(self, item)}')


if __name__ == '__main__':
    oleks = Person(22, 'Oleksandr')
    olga = Person(22, 'Olga')
    oleks.show_age()
    oleks.print_name()
    oleks.show_all_information()
    oleks.profession = 'gym'
    oleks.show_all_information()
    olga.profession = 'HR'
    olga.show_all_information()

