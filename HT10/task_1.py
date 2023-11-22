"""
Банкомат 2.0
- усі дані зберігаються тільки в sqlite3 базі даних. Більше ніяких файлів.
Якщо в попередньому завданні ви добре продумали структуру програми то у вас не
виникне проблем швидко адаптувати її до нових вимог.
- на старті додати можливість залогінитися або створити новго користувача (при
створенні новго користувача, перевіряється відповідність логіну і паролю
мінімальним вимогам. Для перевірки створіть окремі функції)
- в таблиці (базі) з користувачами має бути створений унікальний
користувач-інкасатор, який матиме розширені можливості (домовимось, що
логін/пароль будуть admin/admin щоб нам було простіше перевіряти)
- банкомат має власний баланс
- кількість купюр в банкоматі обмежена. Номінали купюр - 10, 20, 50, 100, 200,
500, 1000
- змінювати вручну кількість купюр або подивитися їх залишок в банкоматі може
лише інкасатор
- користувач через банкомат може покласти на рахунок лише сумму кратну
мінімальному номіналу що підтримує банкомат. В іншому випадку - повернути
"здачу" (наприклад при поклажі 1005 --> повернути 5). Але це не має впливати
на баланс/кількість купюр банкомату, лише збільшуєтсья баланс користувача
(моделюємо наявність двох незалежних касет в банкоматі - одна на прийом, інша
на видачу)
- зняти можна лише в межах власного балансу, але не більше ніж є всього в
банкоматі.
- при неможливості виконання якоїсь операції - вивести повідомлення з причиною
(не вірний логін/пароль, недостатньо коштів на раунку, неможливо видати суму
наявними купюрами тощо.)
"""


import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATABASE_FILE = ('bank.db')
TERMINAL_ID = 1


class ValidationError(ValueError):
    pass


class SignUpError(ValueError):
    pass


class LoginError(BaseException):
    pass


class WithdrawError(BaseException):
    pass


class TerminalError(ValueError):
    pass


def validate_password(password):
    if len(password) < 6:
        raise ValidationError('Password must be longer than 6 characers')
    elif len(password) > 20:
        raise ValidationError('Password must be shorter than 20 characters')
    elif not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain a least 1 digit')
    elif not any(char.isupper() for char in password):
        raise ValidationError('Password must contain a least 1 upper letter')
    elif not any(char.islower() for char in password):
        raise ValidationError('Password must contain a least 1 lower letter')


def validate_username(password):
    if len(password) < 6:
        raise ValidationError('Username must be longer than 6 characers')
    elif len(password) > 20:
        raise ValidationError('Username must be shorter than 20 characters')


def login(username, password):
    if username == 'admin' and password == 'admin':
        return 'admin'
    with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                    SELECT id
                    FROM users WHERE username = ? AND password = ?
            ''', (username, password))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise LoginError('Wrong login or password')


def signup(username, password):
    try:
        validate_username(username)
        validate_password(password)
        with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT id
                    FROM users WHERE username = ?
                ''', (username,))
            if cursor.fetchone():
                raise SignUpError('Username exists')
            else:
                cursor.execute('''
                    INSERT INTO users (username, password, balance)
                            VALUES (?, ?, 0)
                ''', (username, password))
                conn.commit()
        return login(username, password)
    except ValidationError as e:
        raise SignUpError(e)


def withdraw(client_id, amount):
    terminal_balance = ()
    client_balance = 0

    with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                SELECT balance_10, balance_20, balance_50, balance_100,
                       balance_200, balance_500,balance_1000
                FROM terminal_balance WHERE id = ?
            ''', (TERMINAL_ID, ))
        terminal_balance = cursor.fetchone()

    if not terminal_balance:
        raise WithdrawError('Wrong terminal id')

    with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                SELECT balance
                FROM users WHERE id = ?
            ''', (client_id, ))
        client_balance = cursor.fetchone()[0]

    if client_balance < amount:
        raise WithdrawError('Not enough money on balance')

    volumes = (10, 20, 50, 100, 200, 500, 1000)
    total_balance = sum(volume * number for volume, number in zip(
            volumes, terminal_balance)
        )

    if total_balance < amount:
        raise WithdrawError('Terminal balance is lower than withdrawal')

    new_balance = list(terminal_balance)
    new_client_balance = client_balance - amount

    while amount > 0:
        if amount >= volumes[-1] and new_balance[-1]:
            amount -= 1000
            new_balance[-1] -= 1
        elif amount >= volumes[-2] and new_balance[-2]:
            amount -= 500
            new_balance[-2] -= 1
        elif amount >= volumes[-3] and new_balance[-3]:
            amount -= 200
            new_balance[-3] -= 1
        elif amount >= volumes[-4] and new_balance[-4]:
            amount -= 100
            new_balance[-4] -= 1
        elif amount >= volumes[-5] and new_balance[-5]:
            amount -= 50
            new_balance[-5] -= 1
        elif amount >= volumes[-6] and new_balance[-6]:
            amount -= 20
            new_balance[-6] -= 1
        elif amount >= volumes[-7] and new_balance[-7]:
            amount -= 10
            new_balance[-7] -= 1
        else:
            raise WithdrawError('Incorrect withdrawal amount')

    with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = ? WHERE id = ?",
                       (new_client_balance, client_id))
        cursor.execute("""UPDATE terminal_balance SET
                       balance_10 = ?,
                       balance_20 = ?,
                       balance_50 = ?,
                       balance_100 = ?,
                       balance_200 = ?,
                       balance_500 = ?,
                       balance_1000 = ?
                       WHERE id = ?""",
                       (*new_balance, TERMINAL_ID))
        conn.commit()


def deposit(client_id, amount):
    deposit_amount = amount // 10 * 10
    amount = amount % 10

    with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                SELECT balance
                FROM users WHERE id = ?
            ''', (client_id, ))
        client_balance = cursor.fetchone()[0]
        cursor.execute("UPDATE users SET balance = ? WHERE id = ?",
                       (client_balance + deposit_amount, client_id))
        conn.commit()
        print(f'Change: {amount}')


def inq_inspect():
    with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                SELECT balance_10, balance_20, balance_50, balance_100,
                        balance_200, balance_500,balance_1000
                FROM terminal_balance WHERE id = ?
            ''', (TERMINAL_ID, ))
        terminal_balance = cursor.fetchone()
    if not terminal_balance:
        raise TerminalError('Terminal dont exists or broken')
    volumes = (10, 20, 50, 100, 200, 500, 1000)
    print('Current amount of banknotes:')
    for volume, amount in zip(volumes, terminal_balance):
        print(f'Banknote {volume} : {amount}')


def inq_deposit():
    try:
        print('Set new amount of banknotes')
        new_balance = []
        values = (10, 20, 50, 100, 200, 500, 1000)
        for value in values:
            new_balance.append(int(input(f'Amonut of {value} bills: ')))

        with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE terminal_balance SET
                           balance_10 = ?,
                           balance_20 = ?,
                           balance_50 = ?,
                           balance_100 = ?,
                           balance_200 = ?,
                           balance_500 = ?,
                           balance_1000 = ?
                           WHERE id = ?""",
                           (*new_balance, TERMINAL_ID))
        conn.commit()

    except ValueError as e:
        raise TerminalError(e)


def show_user(client_id):
    with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                    SELECT username, balance
                    FROM users WHERE id = ?
            ''', (client_id,))
        user = cursor.fetchone()
        print(f'User: {user[0]} | Balance: {user[1]}')


def menu():
    client_id = None
    menu_dict = {
        type(None): {
            'signup': signup,
            'login': login
        },
        int: {
            'deposit': deposit,
            'withdraw': withdraw,
        },
        str: {
            'inspect': inq_inspect,
            'set bills': inq_deposit
        }
    }
    next_step = ''
    while next_step != 'exit':
        if isinstance(client_id, int):
            show_user(client_id)
        print('Enter name or a number of action:')
        translate_table = {}
        for i, option in zip(
                range(len(menu_dict[type(client_id)])),
                menu_dict[type(client_id)].keys()):
            print(f'{i+1}. {option}')
            translate_table[ord(f'{i+1}')] = option
        print('3. exit')
        next_step = input('Input: ').strip().translate(translate_table)

        if next_step not in menu_dict[type(client_id)].keys()\
                and next_step not in ['exit', '3']:
            print('Wrong action')
            continue

        elif next_step in ['exit', '3']:
            return
        username = input('Username: ') if client_id is None else ''
        password = input('Password: ') if client_id is None else ''
        try:
            amount = int(
                input('Amount: ')) if isinstance(client_id, int) else ''
        except ValueError:
            print('Wrong value')
            continue

        args = []
        for item in [username, password, client_id, amount]:
            if item:
                args.append(item)
        try:
            if not client_id:
                client_id = menu_dict[type(client_id)][next_step](*args)

            elif client_id == 'admin':
                menu_dict[type(client_id)][next_step]()

            else:
                menu_dict[type(client_id)][next_step](*args)

        except SignUpError as e:
            print(e)

        except WithdrawError as e:
            print(e)

        except LoginError as e:
            print(e)

        except TerminalError as e:
            print(e)

        except KeyError:
            print('Wrong action')


def prerun():
    with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                balance INTEGER NOT NULL
            )
            ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS terminal_balance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                balance_10 INTEGER,
                balance_20 INTEGER,
                balance_50 INTEGER,
                balance_100 INTEGER,
                balance_200 INTEGER,
                balance_500 INTEGER,
                balance_1000 INTEGER
            )
        ''')


if __name__ == '__main__':
    prerun()
    menu()
