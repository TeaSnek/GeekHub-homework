"""
Програма-банкомат.
    Використувуючи функції створити програму з наступним функціоналом:
        - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл
        <users.CSV>);
        - кожен з користувачів має свій поточний баланс (файл
        <{amount}_balance.TXT>) та історію транзакцій (файл
        <{username_transactions.JSON>);
        - є можливість як вносити гроші, так і знімати їх. Обов'язкова
        перевірка введених даних (введено цифри; знімається не більше, ніж є
        на рахунку і т.д.).
    Особливості реалізації:
        - файл з балансом - оновлюється кожен раз при зміні балансу (містить
        просто цифру з балансом);
        - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається
        в кінець файла;
        - файл з користувачами: тільки читається. Але якщо захочете реалізувати
        функціонал додавання нового користувача - не стримуйте себе :)
    Особливості функціонала:
        - за кожен функціонал відповідає окрема функція;
        - основна функція - <start()> - буде в собі містити весь workflow
        банкомата:
        - на початку роботи - логін користувача (програма запитує ім'я/пароль).
        Якщо вони неправильні - вивести повідомлення про це і закінчити роботу
        (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на
        ентузіазмі :))
        - потім - елементарне меню типн:
            Введіть дію:
                1. Продивитись баланс
                2. Поповнити баланс
                3. Вихід
        - далі - фантазія і креатив, можете розширювати функціонал, але основне
        завдання має бути повністю реалізоване :)
    P.S. Увага! Файли мають бути саме вказаних форматів (csv, txt, json
    відповідно)
    P.S.S. Добре продумайте структуру програми та функцій
"""

import json
import csv
from datetime import datetime


class LoginError(LookupError):
    pass


class UserExistsError(BaseException):
    pass


def create_user(username, password):
    try:
        with open('HT9/bank_accounts/users.csv', 'r') as users_db:
            reader = csv.DictReader(users_db)
            if any(user['username'] == username for user in reader):
                raise UserExistsError
    except FileNotFoundError:
        raise LoginError('Userfile not found while creating user')
    try:
        with open('HT9/bank_accounts/users.csv', 'a') as users_db:
            print(f'{username},{password}', file=users_db)
        with open(f'HT9/bank_accounts/{username}_balance.txt', 'w')\
                as balance:
            print(.0, file=balance)
        with open(f'HT9/bank_accounts/{username}_transactions.json', 'w')\
                as transactions:
            first_transaction = {
                'type': 'create',
                'time': str(datetime.now()),
                'balance': .0
            }
            print(json.dumps(first_transaction), file=transactions)
    except FileNotFoundError:
        raise LoginError('Userfile not found while creating user')


def login(username, password):
    try:
        with open('HT9/bank_accounts/users.csv', 'r') as users_db:
            reader = csv.DictReader(users_db)
            if {'username': username, 'password': password} not in reader:
                raise LoginError('Incorrect login or password')

    except FileNotFoundError:
        raise LoginError('Userfile not found')


def withdraw(user, amount):
    amount = float(amount)
    if amount <= 0 or not amount == amount:
        raise ValueError('Amount cannot be 0 or less or nan')
    balance = .0
    with open(f'HT9/bank_accounts/{user}_balance.txt', 'r')\
            as b_file:
        balance = float(b_file.read())

    with open(f'HT9/bank_accounts/{user}_balance.txt', 'w')\
            as b_file:
        print(balance - amount if balance >= amount else balance, file=b_file)

    with open(f'HT9/bank_accounts/{user}_transactions.json', 'a')\
            as transactions:
        transaction = {
            'type': 'withdraw',
            'status': 'Success' if balance >= amount else 'Denied',
            'amount': amount,
            'time': str(datetime.now()),
            'balance': balance - amount if balance >= amount else balance,
        }
        print(json.dumps(transaction), file=transactions)
        print(transaction['status'], sep='\n')


def deposit(user, amount):
    amount = float(amount)
    if amount <= 0 or not amount == amount:
        raise ValueError('Amount cannot be 0 or less or nan')
    balance = .0

    with open(f'HT9/bank_accounts/{user}_balance.txt', 'r')\
            as b_file:
        balance = float(b_file.read())

    with open(f'HT9/bank_accounts/{user}_balance.txt', 'w')\
            as b_file:
        print(balance + amount, file=b_file)

    with open(f'HT9/bank_accounts/{user}_transactions.json', 'a')\
            as transactions:
        transaction = {
            'type': 'deposit',
            'status': 'Success',
            'amount': amount,
            'time': str(datetime.now()),
            'balance': balance + amount,
        }
        print(json.dumps(transaction), file=transactions)
        print(transaction['status'], sep='\n')


def current_user(username):
    with open(f'HT9/bank_accounts/{username}_balance.txt', 'r')\
            as b_file:
        balance = float(b_file.read())
        print(f'User: {username}\t Balance: {balance}')


def start():
    logged_in = False
    next_step = ''
    username = ''
    menu = {
        False: {
            'signup': create_user,
            'login': login,
        },
        True: {

            'withdraw': withdraw,
            'deposit': deposit,
        }
    }

    while next_step != 'exit' or next_step != '3':
        try:
            if logged_in:
                current_user(username)
            print('Enter name or a number of action:')
            translate_table = {}
            for i, option in zip(
                    range(len(menu[logged_in])),
                    menu[logged_in].keys()):
                print(f'{i+1}. {option}')
                translate_table[ord(f'{i+1}')] = option
            print('3. exit')
            next_step = input('Input: ').translate(translate_table)
            if next_step not in menu[logged_in].keys()\
                    and next_step not in ['exit', '3']:
                raise KeyError
            elif next_step in ['exit', '3']:
                return

            username = input('Username: ') if not logged_in else username
            second_field = input('Password: ') if not logged_in else\
                input('Amount: ')
            menu[logged_in][next_step](username, second_field)
            logged_in = True

        except LoginError as e:
            print(e)

        except UserExistsError:
            print('Username is already in use')

        except KeyError:
            print('Incorrect action')

        except ValueError:
            print('Incorrect amount inserted')


if __name__ == '__main__':  # start this from "GeekHub homework" directory
    start()
