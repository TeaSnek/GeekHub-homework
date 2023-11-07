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


def login(login, password, silent=False):
    users = [
        {'login': 'Oleksandr', 'password': '12345678'},
        {'login': 'Andrii', 'password': '87654321'},
        {'login': 'GEEKHUB', 'password': 'bogobogo'},
        {'login': 'user123454', 'password': 'qwertyuiop'},
        {'login': '1234', 'password': '1234'}
    ]

    if {'login': login, 'password': password} in users:
        return True
    elif silent:
        return False
    else:
        raise LoginException


if __name__ == '__main__':
    username = input('Input your username: ')
    password = input('Input your password: ')
    print('Successful' if login(username, password) else 'Fail')
