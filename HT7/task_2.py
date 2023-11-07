"""
Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну
   цифру;
   - якесь власне додаткове правило :)
   Якщо якийсь із параментів не відповідає вимогам - породити виключення із
відповідним текстом.
"""


class ValidationError(ValueError):
    pass


def validate(login, password):
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


if __name__ == '__main__':
    print('Login: username | Password: 12345678')
    validate('username', '13245678')
    print('Successfull')

    print('Login: username | Password: qwertyuiop')
    validate('username', 'qwertyuiop')
    print('Successfull')
