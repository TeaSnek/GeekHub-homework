"""
Банкомат 2.0: переробіть программу з функціонального підходу програмування на
використання класів. Додайте шанс 10% отримати бонус на баланс при створенні
нового користувача.
"""

import sqlite3
import requests
from datetime import date
from pathlib import Path
from random import randint as rint

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


class Terminal:
    def __init__(self, terminal_id: int) -> None:
        self.id = terminal_id
        self.balance = self.get_balance()

    def get_balance(self, local=False) -> dict[int, int]:
        if local:
            return self.balance

        with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT balance_10, balance_20, balance_50, balance_100,
                           balance_200, balance_500, balance_1000
                    FROM terminal_balance WHERE id = ?
                ''', (self.id, ))
            terminal_balance = cursor.fetchone()
        if not terminal_balance:
            raise TerminalError('Terminal dont exists or broken')
        volumes = (10, 20, 50, 100, 200, 500, 1000)
        return {volume: amount for volume, amount in
                zip(volumes, terminal_balance)}

    def set_balance(self, b_10, b_20, b_50, b_100, b_200, b_500, b_1000):
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
                           (b_10, b_20,  b_50, b_100, b_200, b_500, b_1000,
                            TERMINAL_ID))
            conn.commit()
        self.balance = self.get_balance()


class User:
    def __init__(self) -> None:
        self.username = None
        self.balance = 0
        self._client_id = None
        self.__superuser = False

    def login(self, username, password):
        if username == 'admin' and password == 'admin':
            self.username = 'admin'
            self.__superuser = True
            return
        with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                        SELECT id, balance
                        FROM users WHERE username = ? AND password = ?
                ''', (username, password))
            result = cursor.fetchone()
            if result:
                self.username = username
                self._client_id = result[0]
                self.balance = result[1]
            else:
                raise LoginError('Wrong login or password')

    def logout(self):
        self.username = None
        self.balance = 0
        self._client_id = None
        self.__superuser = False

    def is_logged(self):
        return not (self.username is None)

    def is_superuser(self):
        return self.__superuser

    def __str__(self) -> str:
        if self.username is None:
            return 'user not loaded'
        return f'username: {self.username} | balance: {self.balance}'

    def get_balance(self):
        if self.is_logged() and not self.is_superuser():
            with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT balance FROM users WHERE id = ?''',
                               (self._client_id, ))
                result = cursor.fetchone()
                if result:
                    self.balance = result[0]
                    return self.balance
                else:
                    raise LoginError('User doesnt exist')
        else:
            raise LoginError('User is not logged in')

    def deposit(self, amount):
        with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance = ? WHERE id = ?",
                           (self.get_balance() + amount,
                            self._client_id))
            conn.commit()
        self.balance += amount

    def withdraw(self, amount):
        with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance = ? WHERE id = ?",
                           (self.get_balance() - amount, self._client_id))
            conn.commit()
        self.balance -= amount


class Interface:
    def __init__(self) -> None:
        self.user = User()
        self.terminal = Terminal(TERMINAL_ID)
        self.state = 'login_menu'

    def start(self):
        while self.state != 'exit':
            self.menu()

    def menu(self):
        if not self.user.is_superuser():
            match self.state:
                case 'login_menu':
                    print('Select your next step:')
                    print('1. Login')
                    print('2. Signup')
                    action = input('Input: ').lower().strip()
                    if action == '0' or action == 'exit':
                        self.state = 'exit'
                        return
                    elif action == '1' or action == 'login':
                        self.state = 'login'
                        return
                    elif action == '2' or action == 'signup':
                        self.state = 'signup'
                        return
                    else:
                        print('Incorrect action')
                        return

                case 'login':
                    username = input('Input your username: ')
                    password = input('Input your password: ')
                    try:
                        self.user.login(username, password)
                    except LoginError as e:
                        print(e)
                        self.state = 'main_menu'
                        return
                    if self.user.is_logged():
                        self.state = 'main_menu'
                        return
                    else:
                        print('Incorrect login or password')
                        self.state = 'login_menu'
                        return

                case 'signup':
                    username = input('Input your username: ')
                    password = input('Input your password: ')
                    try:
                        self.validate_password(password)
                        self.validate_username(username)
                    except ValidationError as e:
                        print(e)
                        self.state = 'login_menu'
                        return
                    self.signup(username, password)
                    return

                case 'main_menu':
                    print(self.user)
                    self.show_exchange_values()
                    print('Select your next step:')
                    print('1. Deposit')
                    print('2. Withdraw')
                    print('3. Logout')
                    action = input('Input: ').lower().strip()
                    if action == '0' or action == 'exit':
                        self.state = 'exit'
                        return
                    elif action == '1' or action == 'deposit':
                        self.state = 'deposit'
                        return
                    elif action == '2' or action == 'withdraw':
                        self.state = 'withdraw'
                        return
                    elif action == '3' or action == 'logout':
                        self.user.logout()
                        self.state = 'login_menu'
                        return
                    else:
                        print('Incorrect action')
                        return

                case 'withdraw':
                    amount = 0
                    try:
                        amount = int(input('Input amount to withdraw: '))
                    except ValueError:
                        print('Incorrect amount')
                        self.state = 'main_menu'
                        return
                    try:
                        self.process_withdrawal(amount)
                        self.state = 'main_menu'
                    except WithdrawError as e:
                        print(e)
                        self.state = 'main_menu'
                        return

                case 'deposit':
                    amount = 0
                    try:
                        amount = int(input('Input amount to deposit: '))
                    except ValueError:
                        print('Incorrect amount')
                        self.state = 'main_menu'
                        return
                    deposit_amount = amount // 10 * 10
                    change = amount % 10
                    if deposit_amount > 0:
                        self.user.deposit(deposit_amount)
                        print(f'Change: {change}')
                        self.state = 'main_menu'
                        return
                    else:
                        print('Incorrect amount')
                        self.state = 'main_menu'
                        return
        else:
            match self.state:
                case 'main_menu':
                    print('Select your next step:')
                    print('1. Inspect')
                    print('2. Set balance')
                    print('3. Logout')
                    action = input('Input: ').lower().strip()
                    if action == '0' or action == 'exit':
                        self.state = 'exit'
                        return
                    elif action == '1' or action == 'inspect':
                        self.state = 'inspect'
                        return
                    elif action == '2' or action == 'set_balance':
                        self.state = 'set_balance'
                        return
                    elif action == '3' or action == 'logout':
                        self.user.logout()
                        self.state = 'login_menu'
                        return
                    else:
                        print('Incorrect action')
                        return

                case 'inspect':
                    terminal_balance = self.terminal.get_balance(local=True)
                    print('Current amount of banknotes (local):')
                    for volume, amount in terminal_balance.items():
                        print(f'Banknote {volume} : {amount}')
                    terminal_balance = self.terminal.get_balance()
                    print('Current amount of banknotes (server):')
                    for volume, amount in terminal_balance.items():
                        print(f'Banknote {volume} : {amount}')
                    self.state = 'main_menu'

                case 'set_balance':
                    print('Set new amount of banknotes')
                    new_balance = []
                    values = (10, 20, 50, 100, 200, 500, 1000)
                    try:
                        for value in values:
                            new_balance.append(int(input(
                                f'Amounut of {value} bills: ')))
                    except ValueError:
                        print('Incorrect amount')
                    self.terminal.set_balance(*new_balance)
                    self.state = 'main_menu'

    def signup(self, username, password):
        with sqlite3.connect(Path(BASE_DIR, DATABASE_FILE)) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT id
                    FROM users WHERE username = ?
                ''', (username,))
            if cursor.fetchone():
                print('Username exists')
                self.state = 'login_menu'
                return
            else:
                start_balance = 50 if rint(1, 10) == 10 else 0
                cursor.execute('''
                    INSERT INTO users (username, password, balance)
                            VALUES (?, ?, ?)''', (
                                username, password, start_balance
                    ))
                conn.commit()
                self.user.login(username, password)
                self.state = 'main_menu'

    def process_withdrawal(self, amount):
        if self.user.balance < amount:
            raise WithdrawError('Withdraw amount is higher than balance')

        balance_diff = self.withdraw_from_balance(amount)
        new_balance = [x - y for x, y in zip(self.terminal.balance.values(),
                                             balance_diff)]
        self.user.withdraw(amount)
        self.terminal.set_balance(*new_balance)
        values = (10, 20, 50, 100, 200, 500, 1000)
        print('Withdrawed:')
        for key, value in zip(values, balance_diff):
            print(f'{key} x{value}')
        return True

    def withdraw_from_balance(self, amount: int) -> list[int]:
        total_sum = sum(key * value for key, value in
                        self.terminal.get_balance().items())
        if total_sum < amount:
            raise WithdrawError('Not enough banknotes in terminal')
        keys = list(self.terminal.balance.keys())
        start = max(i for i in range(len(keys))
                    if self.terminal.balance[keys[i]] != 0)
        while start != 0:
            diff_values = [0] * len(keys)
            change = amount
            while change:
                try:
                    undo_key = min(keys[i] for i in range(len(keys))
                                   if diff_values[i] != 0)
                    change += undo_key
                    diff_values[keys.index(undo_key)] -= 1
                    i = keys.index(undo_key) - 1
                except ValueError:
                    undo_key = keys[start]
                    i = start
                if undo_key == min(key for key, value in
                                   self.terminal.balance.items()
                                   if value != 0):
                    break
                while i >= 0:
                    diff_values[i] += min(change//keys[i],
                                          self.terminal.balance[keys[i]])
                    change -= keys[i] * diff_values[i]
                    if change == 0:
                        return diff_values
                    i -= 1
            start -= 1
        raise WithdrawError('Impossible to withdraw')

    @staticmethod
    def validate_password(password):
        if len(password) < 6:
            raise ValidationError(
                'Password must be longer than 6 characers')
        elif len(password) > 20:
            raise ValidationError(
                'Password must be shorter than 20 characters')
        elif not any(char.isdigit() for char in password):
            raise ValidationError(
                'Password must contain a least 1 digit')
        elif not any(char.isupper() for char in password):
            raise ValidationError(
                'Password must contain a least 1 upper letter')
        elif not any(char.islower() for char in password):
            raise ValidationError(
                'Password must contain a least 1 lower letter')

    @staticmethod
    def validate_username(username):
        if len(username) < 6:
            raise ValidationError(
                'Username must be longer than 6 characers')
        elif len(username) > 20:
            raise ValidationError(
                'Username must be shorter than 20 characters')

    @staticmethod
    def show_exchange_values():
        time_template = '%Y-%m-%d'
        exchange_data_list = []
        try:
            with open(Path(BASE_DIR, 'exc.txt'), 'r') as file:
                text_update_date = file.readline()
                if text_update_date == date.today().strftime(time_template):
                    for line in file:
                        exchange_data_list.append(line)
        except FileNotFoundError:
            pass

        if not exchange_data_list:
            request = requests.get(
                'https://api.privatbank.ua/p24api/pubinfo?exchange',
                params={'coursid': '5'})
            request_data = request.json()
            for cur in request_data:
                exchange_data_list.append(
                    '{} {:.2f} / {:.2f}'.format(
                        cur['ccy'],
                        float(cur['buy']),
                        float(cur['sale'])
                    )
                )
            update_date = date.today().strftime(time_template)
            with open(Path(BASE_DIR, 'exc.txt'), 'w') as file:
                print(update_date, file=file)
                for line in exchange_data_list:
                    print(line, file=file)

        for line in exchange_data_list:
            print(line)


if __name__ == '__main__':
    session = Interface()
    session.start()
