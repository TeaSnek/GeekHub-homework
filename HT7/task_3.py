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

from task_2 import validate, ValidationError

USERS = {
      'Oleksandr': '12345678',
      'Andrii': '87654321',
      'GEEKHUB': 'bogobogo',
      'user123454': 'qwertyuiop',
      '1234': '1234'
    }


if __name__ == '__main__':
    for item in USERS.items():
        print(f'Name: {item[0]}\nPassword: {item[1]}')
        try:
            validate(*item)
            print('Status: OK')
        except ValidationError as e:
            print(f'Status: {e}')
        print()
