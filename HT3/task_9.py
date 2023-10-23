"""
Користувачем вводиться початковий і кінцевий рік. Створити цикл, який виведе
всі високосні роки в цьому проміжку (границі включно). P.S. Рік є високосним,
якщо він кратний 4, але не кратний 100, а також якщо він кратний 400.
"""


if __name__ == '__main__':
    from_year = int(input('Input starting year: '))
    to_year = int(input('Input last year to count: '))
    for year in range(from_year, to_year+1):
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            print(year, end=' ')
