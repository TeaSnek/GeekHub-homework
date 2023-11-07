"""
На основі попередньої функції (скопіюйте кусок коду) створити наступний
скрипт:

а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь по
правилам своєї функції) - як валідні, так і ні;
б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором,
перевірить ці дані і надрукує для кожної пари значень відповідне повідомлення,
наприклад:

      Name: vasya
      Password: wasd
      Status: password must have at least one digit
      -----
      Name: vasya
      Password: vasyapupkin2000
      Status: OK

P.S. Не забудьте використати блок try/except ;)
"""


class ValidationError(ValueError):
    pass


def validate(login: str, password: str):
    if 3 >= len(login):
        raise ValidationError('Login must be longer than 3 characters')

    elif len(login) >= 50:
        raise ValidationError('Login must be shorter than 50 characters')

    elif len(password) < 8:
        raise ValidationError('Password should be shorter than 8 characters')

    elif not any(char.isdigit() for char in password):
        raise ValidationError('Password should contain at least 1 number')

    elif any(symbol in password for symbol in ['`', '$', '|']):
        raise ValidationError('Password cannot contain special characters')


USERS = [
        {'login': 'Oleksandr', 'password': '12345678'},
        {'login': 'Andrii', 'password': '87654321'},
        {'login': 'GEEKHUB', 'password': 'bogobogo'},
        {'login': 'user123454', 'password': 'qwertyuiop'},
        {'login': '1234', 'password': '1234'}
    ]


if __name__ == '__main__':
    for item in USERS:
        print(f'Name: {item['login']}\nPassword: {item['password']}')
        try:
            validate(**item)
            print('Status: OK')
        except ValidationError as e:
            print(f'Status: {e}')
        print()
