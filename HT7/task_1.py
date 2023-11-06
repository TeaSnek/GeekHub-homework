"""
Створіть функцію, всередині якої будуть записано список із п'яти користувачів
(ім'я та пароль). Функція повинна приймати три аргументи: два - обов'язкових
(<username> та <password>) і третій - необов'язковий параметр <silent>
(значення за замовчуванням - <False>).
Логіка наступна:
    якщо введено коректну пару ім'я/пароль - вертається True;
    якщо введено неправильну пару ім'я/пароль:
        якщо silent == True - функція вертає False
        якщо silent == False -породжується виключення LoginException (його
        також треба створити =))
"""


class LoginException(BaseException):
    pass


def login(username, password, silent=False):
    users = {
        'Oleksandr': '12345678',
        'Andrii': '87654321',
        'GEEKHUB': 'bogobogo',
        'user123454': 'qwertyuiop',
        '1234': '1234'
    }

    if users[username] == password:
        return True
    elif silent:
        return False
    else:
        raise LoginException


if __name__ == '__main__':
    username = input('Input your username: ')
    password = input('Input your password: ')
    print('Successful' if login(username, password) else 'Fail')
