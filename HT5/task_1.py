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
    for i in range(-1, 14):
        print(i, season(i))
