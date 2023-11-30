"""
Створіть за допомогою класів та продемонструйте свою реалізацію шкільної
бібліотеки (включіть фантазію).
"""

import sqlite3 as db
from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).parent
DB_FILE = 'library.db'


class ValidationError(AssertionError):
    ...


class Book:
    def __init__(self, name: str, author: str, genre='', short_about='',
                 year_of_prod='Unknown') -> None:
        self.name = name.lower()
        self.author = author.lower()
        self.genre = genre.lower()
        self.short_about = short_about.lower()
        self.year_of_prod = year_of_prod.lower()

    def __str__(self) -> str:
        return '\n'.join(f'{field.capitalize()}: {value.capitalize()}'
                         for field, value
                         in self.__dict__.items() if value)


class User:
    connect = db.connect(Path(BASE_DIR, DB_FILE))

    def __init__(self, username='', first_name='', last_name='',
                 usertype='unlogged') -> None:
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.type = usertype

    def login(self, username: str, password: str) -> None:
        cur = self.connect.cursor()
        cur.execute("""select first_name, last_name, type from users
                       where username = ? and password = ?""",
                    (username, password))
        result = cur.fetchone()
        if result:
            self.first_name, self.last_name, self.type = result
            self.username = username
        else:
            raise KeyError('Wrong login or password')

    def signup(self, username: str, password: str,
               first_name: str, last_name: str) -> None:
        self.validate_password(password)
        self.validate_username(password)
        cur = self.connect.cursor()
        cur.execute('''select username from users
                    where username = ? and type = ?''',
                    (username, 'user'))
        if cur.fetchone():
            raise ValidationError('Username already exists')
        cur.execute("""
                    insert into users
                    (username, password, first_name, last_name, type)
                    values (?, ?, ?, ?, ?)""",
                    (username, password, first_name, last_name, 'user'))
        self.connect.commit()
        self.login(username, password)

    def super_signup(self, username: str, password: str,
                     first_name: str, last_name: str) -> None:
        cur = self.connect.cursor()
        cur.execute('select username from users where username = ?, type = ?',
                    (username, 'user'))
        if cur.fetchone():
            raise ValidationError('Username already exists')
        self.validate_password(password)
        self.validate_username(password)
        cur.execute("""
                    insert into users
                    (username, password, first_name, last_name, type)
                    values (?, ?, ?, ?, ?)""",
                    (username, password, first_name, last_name, 'super'))
        self.connect.commit()
        self.login(username, password)

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


class Storage:
    books = []
    conn = db.connect(Path(BASE_DIR, DB_FILE))

    def __init__(self) -> None:
        self.prerun()
        if not self.books:
            self.books = self.load_books()

    def prerun(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                type TEXT NOT NULL
            )
            ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                short_about TEXT NOT NULL,
                year_of_prod TEXT NOT NULL,
                state TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    @staticmethod
    def load_books():
        cur = Storage.conn.cursor()
        cur.execute('''SELECT id, name, author, genre, short_about,
                    year_of_prod, state FROM books''')
        result = cur.fetchall()
        return [
            {
                'book_id': book_id,
                'book': Book(
                        name,
                        author,
                        genre,
                        short_about,
                        year_of_prod),
                'state': json.loads(state)
            } for book_id, name, author, genre,
            short_about, year_of_prod, state in result]

    def add_book(self, book: Book):
        cur = self.conn.cursor()
        cur.execute('''insert into books (name, author, genre, short_about,
                    year_of_prod, state) values (?, ?, ?, ?, ?, ?)''',
                    (book.name, book.author, book.genre, book.short_about,
                     book.year_of_prod, book.year_of_prod,
                     json.dumps({'belongs': 'library'})))
        self.conn.commit()
        self.books = self.load_books()

    def del_book(self, book_id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM books WHERE id = ?', (book_id,))
        self.conn.commit()
        self.books = self.load_books()

    def search_book(self, **kwargs):
        return {book['book_id']: book['book'] for book in self.books
                if all(getattr(book['book'], attr) == value
                       for attr, value in kwargs.items())
                and book['state'] == {'belongs': 'library'}}

    def get_books(self):
        return list(set(book['book'] for book in self.books
                        if book['state'] == {'belongs': 'library'}))

    def lend_book(self, user: User, book_id: int):
        book_index = self.books.index([book for book in self.books
                                       if book['book_id'] == book_id][0]) - 1
        self.books[book_index]['state'] = {
            'belongs': user.username,
            'lend_date': datetime.now().strftime('%d/%m/%Y')
            }

    def __del__(self):
        """
        saves storage to db when destructed
        """
        cur = self.conn.cursor()
        for book in self.books:
            cur.execute("""INSERT OR REPLACE INTO books
                        (id, name, author, genre, short_about, year_of_prod,
                        state) values (?, ?, ?, ?, ?, ?, ?)""",
                        (book['book_id'], *book['book'].__dict__.values(),
                         json.dumps(book['state'])))
        self.conn.commit()


class Terminal:
    def __init__(self) -> None:
        self.__storage = Storage()
        self.__state = 'login_menu'
        self.cur_user = User()

    def start(self):
        while self.__state != 'exit':
            self.menu()

    def menu(self):
        match self.__state:
            case 'login_menu':
                print('1. Login')
                print('2. SignUp')
                print('3. Exit')
                step = input('Input: ')
                match step:
                    case '1':
                        self.__state = 'login'
                    case '2':
                        self.__state = 'signup'
                    case '3':
                        self.__state = 'exit'
                    case _:
                        print('Wrong input')
            case 'signup':
                username = input('Username: ')
                password = input('Password: ')
                first_name = input('Your first name: ')
                last_name = input('Your last name: ')
                try:
                    self.cur_user.signup(username, password, first_name,
                                         last_name)
                    self.__state = 'main_menu'
                except ValidationError as e:
                    print(e)
                    self.__state = 'login_menu'
            case 'login':
                username = input('Username: ')
                password = input('Password: ')
                try:
                    self.cur_user.login(username, password)
                    self.__state = 'main_menu'
                except KeyError as e:
                    print(e)
                    self.__state = 'login_menu'
            case 'main_menu':
                print('1. Search book')
                print('2. Lend book')
                print('3. Get all books')
                print('4. Logout')
                next_step = input('Input: ')
                match next_step.strip():
                    case '1':
                        self.__state = 'search_book'
                    case '2':
                        self.__state = 'lend_book'
                    case '3':
                        self.__state = 'get_books'
                    case '4':
                        self.__state = 'logout'
                    case _:
                        print('Wrong action')
            case 'search_book':
                name = input('Name: Any\033[3D')
                author = input('Author: Any\033[3D')
                req = {
                    'name': name.lower(),
                    'author': author.lower(),
                }
                search = self.__storage.search_book(**{key: value
                                                       for key, value
                                                       in req.items() if value}
                                                    )
                print(*[f'ID\n{key}: {book}' for key, book in search.items()],
                      sep='\n----------------------------\n')
                self.__state = 'main_menu'
            case 'lend_book':
                book_id = 0
                try:
                    book_id = int(input('Input book id: '))
                except ValueError:
                    print('Wrong book id')
                    return
                self.__storage.lend_book(self.cur_user, book_id)
                self.__state = 'main_menu'
            case 'get_books':
                search = self.__storage.get_books()
                print(*search, sep='\n_____________________\n')
                self.__state = 'main_menu'
            case 'logout':
                self.cur_user = User()
                self.__state = 'login_menu'
            case _:
                raise KeyError(f'Unexpected terminal state {self.__state}')


if __name__ == '__main__':
    ter = Terminal()
    ter.start()
