"""
Написати функцiю season, яка приймає один аргумент (номер мiсяця вiд 1 до 12)
та яка буде повертати пору року, якiй цей мiсяць належить (зима, весна, лiто
або осiнь). У випадку некоректного введеного значення - виводити відповідне 
повідомлення.
"""


def season(month_num : int) -> str:
    if month_num not in range(1, 13):
        return 'incorrect month number'
    return ['spring', 'summer', 'fall', 'winter'][(month_num+1)//3-1]


if __name__ == '__main__':
    month_num = 0
    while not 1<=month_num<=12:
        try:
            month_num = int(input('Input correct month number: '))
        except ValueError:
            month_num = 0
    print(season(month_num))
    